import os
import unittest

import pandas as pd

from similarity_framework.src.impl.comparator.comparator_by_type import HausdorffDistanceMin, SizeHandler, get_ratio, ComparatorByType, \
    ColumnExactNamesHandler, ColumnNamesEmbeddingsHandler, IncompleteColumnsHandler, KindHandler
from similarity_framework.src.impl.comparator.comparator_by_column import (ComparatorByColumn, SizeHandler as SizeHandlerByColumn,
                                                      IncompleteColumnsHandler as IncompleteColumnsHandlerByColumn,
                                                      ColumnNamesEmbeddingsHandler as ColumnNamesEmbeddingsHandlerByColumn,
                                                      ColumnExactNamesHandler as ColumnExactNamesHandlerByColumn,
                                                      ColumnKindHandler, ColumnEmbeddingsHandler
                                                      )
from similarity_framework.src.impl.comparator.distance_functions import AverageDist
from similarity_framework.src.impl.comparator.utils import concat, cosine_sim, fill_result, are_columns_null, create_string_from_columns
from similarity_framework.src.models.metadata import MetadataCreatorInput
from similarity_framework.src.models.similarity import Settings
from similarity_framework.src.impl.metadata.type_metadata_creator import TypeMetadataCreator
from similarity_framework.src.models.types_ import DataKind

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class TestFunctions(unittest.TestCase):
    def test_concat(self):
        df1 = pd.DataFrame([(1, 3, 3), (2, 1, 4), (2, 5, 1)])
        df2 = pd.DataFrame([(2, 3, 3), (1, 4, 2), (5, 1, 2)])
        df3 = pd.DataFrame([(3, 1, 2), (2, 1, 5), (2, 4, 1)])
        res = concat(df1, df2, df3).map(lambda x: round(x, 2))

        w_outcome = pd.DataFrame([(2, 2.33, 2.67), (1.67, 2, 3.67), (3, 3.33, 1.33)])
        self.assertTrue(res.equals(w_outcome))

    def test_hausdorff_min(self):
        df1 = pd.DataFrame([(2, 3, 3), (1, 4, 2), (5, 1, 2)])
        df2 = pd.DataFrame([(7, 2, 2), (8, 3, 4), (9, 2, 5)])
        df3 = pd.DataFrame([(1, 1, 3), (1, 2, 3), (1, -1, 2)])
        df4 = pd.DataFrame([(5, 3, 4), (2, 8, 8), (1, 100, 100)])
        self.assertEqual(HausdorffDistanceMin().compute(df1), 2)
        self.assertEqual(HausdorffDistanceMin().compute(df2), 3)
        self.assertEqual(HausdorffDistanceMin().compute(df3), 1)
        self.assertEqual(HausdorffDistanceMin().compute(df4), 3)

    def test_average_dist(self):
        df1 = pd.DataFrame([(2, 3, 3), (1, 4, 2), (5, 1, 2)])
        df2 = pd.DataFrame([(7, 2, 2), (8, 3, 4), (9, 2, 5)])
        df3 = pd.DataFrame([(1, 1, 3), (1, 2, 3), (1, -1, 2)])
        df4 = pd.DataFrame([(5, 3, 4), (2, 8, 8), (1, 100, 100)])
        self.assertEqual(AverageDist().compute(df1), 4/3)
        self.assertEqual(AverageDist().compute(df2), 7/3)
        self.assertEqual(AverageDist().compute(df3), 1/3)
        self.assertEqual(AverageDist().compute(df4), 6/3)

    def test_get_ratio(self):
        self.assertEqual(round(get_ratio(3, 5), 2), 1.67)
        self.assertEqual(round(get_ratio(5, 3), 2), 1.67)
        self.assertEqual(round(get_ratio(15, 9), 2), 1.67)
        self.assertEqual(round(get_ratio(9, 15), 2), 1.67)

    def test_cosine_sim(self):
        self.assertEqual(cosine_sim([1, 2, 3], [1, 2, 3]), 1)
        self.assertEqual(cosine_sim([1, 2, 3], [3, 2, 1]), 0.714)
        self.assertEqual(cosine_sim([1, 2, 3], [1, 2, 4]), 0.991)
        self.assertEqual(cosine_sim([1, 2, 3], [1, 2, 2]), 0.98)
        self.assertEqual(cosine_sim([1, 2, 3], [-1, -2, -3]),  -1)

    def test_fill_result(self):
        metadata1_names = {0: 'a', 1: 'b', 2: 'c'}
        metadata2_names = {0: 'a', 1: 'b', 2: 'd'}
        data = {
            0: [0.0, 1.0, 1.0],
            1: [1.0, 0.0, 1.0],
            2: [1.0, 1.0, 1.0]
        }

        res = pd.DataFrame(data)
        print(res)
        self.assertTrue(fill_result(metadata1_names, metadata2_names).equals(res))

    def test_create_string_from_columns(self):
        # Create sample data
        df1 = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': [4, 5, 6]
        })
        df2 = pd.DataFrame({
            'col1': [7, 8, 9],
            'col2': [10, 11, 12]
        })
        database = [df1, df2]
        table_names = ['table1', 'table2']

        # Expected results
        expected_sentences = [
            '1, 2, 3', '4, 5, 6',
            '7, 8, 9', '10, 11, 12'
        ]
        expected_sentences_datasets = [
            'table1', 'table1',
            'table2', 'table2'
        ]

        # Run the function
        sentences, sentences_datasets = create_string_from_columns(database, table_names)

        # Assert the results
        self.assertEqual(sentences, expected_sentences)
        self.assertEqual(sentences_datasets, expected_sentences_datasets)

class TestAreColumnsNull(unittest.TestCase):
    def test_both_columns_empty(self):
        self.assertEqual(are_columns_null(set(), set(), "Test message"), (True, 0))

    def test_first_column_empty(self):
        self.assertEqual(are_columns_null(set(), {1, 2, 3}, "Test message"), (True, 1))

    def test_second_column_empty(self):
        self.assertEqual(are_columns_null({1, 2, 3}, set(), "Test message"), (True, 1))

    def test_both_columns_non_empty(self):
        self.assertEqual(are_columns_null({1, 2, 3}, {4, 5, 6}, "Test message"), (False, 0))


class TestSingleSpecificComparator(unittest.TestCase):
    def setUp(self):
        self.compartor = ComparatorByType()

        self.file = os.path.join(THIS_DIR, '../data_validation/edge_cases.csv')
        self.data = pd.read_csv(self.file)
        self.data_diff_column_names = self.data.copy()
        self.data_diff_column_names.columns = [f"column_{i}" for i in range(len(self.data.columns))]
        self.data_first_half = self.data.iloc[:int(len(self.data) / 2), :]
        self.data_second_half = self.data.iloc[int(len(self.data) / 2):, :].copy()
        self.data_second_half.index = self.data_second_half.index - int(len(self.data) / 2)
        self.data_diff_type = self.data.copy()  # todo fill

        self.metadata_creator = (TypeMetadataCreator()
                                 .compute_advanced_structural_types()
                                 .compute_column_kind()
                                 .compute_advanced_structural_types()
                                 .compute_incomplete_column()
                                 .compute_column_names_embeddings())
        self.metadata1 = self.metadata_creator.get_metadata(MetadataCreatorInput(dataframe=self.data))
        self.metadata_diff_column_names = self.metadata_creator.get_metadata(MetadataCreatorInput(dataframe=self.data_diff_column_names))
        self.metadata_first_half = self.metadata_creator.get_metadata(MetadataCreatorInput(dataframe=self.data_first_half))
        self.metadata_second_half = self.metadata_creator.get_metadata(MetadataCreatorInput(dataframe=self.data_second_half))

    def test_size_compare(self):
        self.compartor.add_comparator_type(SizeHandler())

        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata1).distance, 0)
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata_diff_column_names).distance, 0)
        self.assertEqual(self.compartor.compare(self.metadata_first_half, self.metadata_second_half).distance, 0)
        self.compartor.add_settings(Settings.NO_RATIO)
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata1).distance, 0)
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata_diff_column_names).distance, 0)
        self.assertEqual(self.compartor.compare(self.metadata_first_half, self.metadata_second_half).distance, 0)

    def test_incomplete_compare(self):
        self.compartor.add_comparator_type(IncompleteColumnsHandler())

        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata1).distance, 0)
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata_diff_column_names).distance, 0)
        self.assertEqual(self.compartor.compare(self.metadata_first_half, self.metadata_second_half).distance, 0)
        self.compartor.add_settings(Settings.NO_RATIO)
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata1).distance, 0)
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata_diff_column_names).distance, 0)
        self.assertEqual(self.compartor.compare(self.metadata_first_half, self.metadata_second_half).distance, 0)

    def test_exact_names_compare(self):
        self.compartor.add_comparator_type(ColumnExactNamesHandler())
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata1).distance, 0)
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata_diff_column_names).distance, 1)
        self.assertEqual(self.compartor.compare(self.metadata_first_half, self.metadata_second_half).distance, 0)
        self.compartor.add_settings(Settings.NO_RATIO)
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata1).distance, 0)
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata_diff_column_names).distance, 1)
        self.assertEqual(self.compartor.compare(self.metadata_first_half, self.metadata_second_half).distance, 0)

    def test_embeddings_names_compare(self):
        self.compartor.add_comparator_type(ColumnNamesEmbeddingsHandler())
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata1).distance, 0)
        self.compartor.add_settings(Settings.NO_RATIO)
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata1).distance, 0)

    def test_kind_compare(self):
        self.compartor.add_comparator_type(KindHandler())

        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata1).distance, 0)
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata_diff_column_names).distance, 0)
        # self.assertEqual(self.compartor.compare(self.metadata_first_half, self.metadata_second_half), 0)
        self.compartor.add_settings(Settings.NO_RATIO)
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata1).distance, 0)
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata_diff_column_names).distance, 0)
        # self.assertEqual(self.compartor.compare(self.metadata_first_half, self.metadata_second_half), 0)

    def test_kind_BOOL_compare(self):
        self.compartor.add_comparator_type(KindHandler(compare_kind=[DataKind.BOOL]))
        self.assertEqual(
            self.compartor.compare(self.metadata1, self.metadata1).distance, 0)
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata_diff_column_names).distance, 0)
        self.assertEqual(self.compartor.compare(self.metadata_first_half, self.metadata_second_half).distance, 0)

    def test_kind_ID_compare(self):
        self.compartor.add_comparator_type(KindHandler(compare_kind=[DataKind.ID]))
        self.assertEqual(
            self.compartor.compare(self.metadata1, self.metadata1).distance, 0)
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata_diff_column_names).distance, 0)

    def test_kind_CATEGORICAL_compare(self):
        self.compartor.add_comparator_type(KindHandler(compare_kind=[DataKind.CATEGORICAL]))
        self.assertEqual(
            self.compartor.compare(self.metadata1, self.metadata1).distance, 0)
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata_diff_column_names).distance, 0)
        self.assertEqual(self.compartor.compare(self.metadata_first_half, self.metadata_second_half).distance, 0)

    def test_kind_CONSTANT_compare(self):
        self.compartor.add_comparator_type(KindHandler(compare_kind=[DataKind.CONSTANT]))
        self.assertEqual(
            self.compartor.compare(self.metadata1, self.metadata1).distance, 0)
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata_diff_column_names).distance, 0)
        self.assertEqual(self.compartor.compare(self.metadata_first_half, self.metadata_second_half).distance, 0)


class TestSingleSpecificComparatorByColumn(TestSingleSpecificComparator):
    def setUp(self):
        self.compartor = ComparatorByColumn()
        self.file = os.path.join(THIS_DIR, '../data_validation/edge_cases.csv')
        self.data = pd.read_csv(self.file)
        self.data_diff_column_names = self.data.copy()
        self.data_diff_column_names.columns = [f"column_{i}" for i in range(len(self.data.columns))]
        self.data_first_half = self.data.iloc[:int(len(self.data) / 2), :]
        self.data_second_half = self.data.iloc[int(len(self.data) / 2):, :].copy()
        self.data_second_half.index = self.data_second_half.index - int(len(self.data) / 2)
        self.data_diff_type = self.data.copy()  # todo fill

        self.metadata_creator = (TypeMetadataCreator()
                                 .compute_advanced_structural_types()
                                 .compute_column_kind()
                                 .compute_incomplete_column()
                                 .compute_column_kind()
                                 .compute_column_names_embeddings()
                                 .compute_column_embeddings()
                                )
        self.metadata1 = self.metadata_creator.get_metadata(MetadataCreatorInput(dataframe=self.data))

        self.metadata_diff_column_names = self.metadata_creator.get_metadata(MetadataCreatorInput(dataframe=self.data_diff_column_names))

        self.metadata_first_half = self.metadata_creator.get_metadata(MetadataCreatorInput(dataframe=self.data_first_half))

        self.metadata_second_half = self.metadata_creator.get_metadata(MetadataCreatorInput(dataframe=self.data_second_half))

    def test_size_compare(self):
        self.compartor.add_comparator_type(SizeHandlerByColumn())

        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata1).distance, 0)
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata_diff_column_names).distance, 0)
        self.assertEqual(self.compartor.compare(self.metadata_first_half, self.metadata_second_half).distance, 0)
        self.compartor.add_settings(Settings.NO_RATIO)
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata1).distance, 0)
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata_diff_column_names).distance, 0)
        self.assertEqual(self.compartor.compare(self.metadata_first_half, self.metadata_second_half).distance, 0)

    def test_incomplete_compare(self):
        self.compartor.add_comparator_type(IncompleteColumnsHandlerByColumn())
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata1).distance, 0)
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata_diff_column_names).distance, 0)
        self.assertEqual(self.compartor.compare(self.metadata_first_half, self.metadata_second_half).distance, 0)
        self.compartor.add_settings(Settings.NO_RATIO)
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata1).distance, 0)
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata_diff_column_names).distance, 0)
        self.assertEqual(self.compartor.compare(self.metadata_first_half, self.metadata_second_half).distance, 0)

    def test_exact_names_compare(self):
        self.compartor.add_comparator_type(ColumnExactNamesHandlerByColumn())
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata1).distance, 0)
        # self.assertEqual(self.compartor.compare(self.metadata1, self.metadata_diff_column_names).distance, 1) #todo fix
        self.assertEqual(self.compartor.compare(self.metadata_first_half, self.metadata_second_half).distance, 0)
        self.compartor.add_settings(Settings.NO_RATIO)
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata1).distance, 0)
        # self.assertEqual(self.compartor.compare(self.metadata1, self.metadata_diff_column_names).distance, 1)
        self.assertEqual(self.compartor.compare(self.metadata_first_half, self.metadata_second_half).distance, 0)

    def test_embeddings_names_compare(self):
        self.compartor.add_comparator_type(ColumnNamesEmbeddingsHandlerByColumn())
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata1).distance, 0)
        self.compartor.add_settings(Settings.NO_RATIO)
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata1).distance, 0)

    def test_kind_compare(self):
        self.compartor.add_comparator_type(ColumnKindHandler())

        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata1).distance, 0)
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata_diff_column_names).distance, 0)
        self.compartor.add_settings(Settings.NO_RATIO)
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata1).distance, 0)
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata_diff_column_names).distance, 0)

    def test_kind_BOOL_compare(self):
        self.compartor.add_comparator_type(ColumnKindHandler([DataKind.BOOL]))
        self.assertEqual(
            self.compartor.compare(self.metadata1, self.metadata1).distance, 0)
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata_diff_column_names).distance, 0)
        self.assertEqual(self.compartor.compare(self.metadata_first_half, self.metadata_second_half).distance, 0)

    def test_kind_ID_compare(self):
        self.compartor.add_comparator_type(ColumnKindHandler([DataKind.ID]))
        self.assertEqual(
            self.compartor.compare(self.metadata1, self.metadata1).distance, 0)
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata_diff_column_names).distance, 0)

    def test_kind_CATEGORICAL_compare(self):
        self.compartor.add_comparator_type(ColumnKindHandler([DataKind.CATEGORICAL]))
        self.assertEqual(
            self.compartor.compare(self.metadata1, self.metadata1).distance, 0)
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata_diff_column_names).distance, 0)
        self.assertEqual(self.compartor.compare(self.metadata_first_half, self.metadata_second_half).distance, 0)

    def test_kind_CONSTANT_compare(self):
        self.compartor.add_comparator_type(ColumnKindHandler([DataKind.CONSTANT]))
        self.assertEqual(
            self.compartor.compare(self.metadata1, self.metadata1).distance, 0)
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata_diff_column_names).distance, 0)
        self.assertEqual(self.compartor.compare(self.metadata_first_half, self.metadata_second_half).distance, 0)

    def test_embedding_compare(self):
        comparator = ComparatorByColumn()
        comparator.add_comparator_type(ColumnEmbeddingsHandler())
        self.assertEqual(comparator.compare(self.metadata1, self.metadata1).distance, 0)
        comparator.add_settings(Settings.NO_RATIO)
        self.assertEqual(comparator.compare(self.metadata1, self.metadata1).distance, 0)


if __name__ == '__main__':
    unittest.main()
