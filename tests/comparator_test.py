import unittest

import pandas as pd

from similarity.Comparator import HausdorffDistanceMin, SizeComparator, get_ratio, Comparator, Settings, \
    ColumnExactNamesComparator, ColumnNamesEmbeddingsComparator, IncompleteColumnsComparator, KindComparator
from similarity.DataFrameMetadataCreator import DataFrameMetadataCreator
from similarity.Types import DataKind


class TestFunctions(unittest.TestCase):
    def test_concat(self):
        df1 = pd.DataFrame([(1, 3, 3), (2, 1, 4), (2, 5, 1)])
        df2 = pd.DataFrame([(2, 3, 3), (1, 4, 2), (5, 1, 2)])
        df3 = pd.DataFrame([(3, 1, 2), (2, 1, 5), (2, 4, 1)])
        res = SizeComparator().concat(df1, df2, df3).map(lambda x: round(x, 2))

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

    def test_get_ratio(self):
        self.assertEqual(round(get_ratio(3, 5), 2), 1.67)
        self.assertEqual(round(get_ratio(5, 3), 2), 1.67)
        self.assertEqual(round(get_ratio(15, 9), 2), 1.67)
        self.assertEqual(round(get_ratio(9, 15), 2), 1.67)


class TestSingleSpecificComparator(unittest.TestCase):
    def setUp(self):
        self.compartor = Comparator()
        self.file = "../data_validation/edge_cases.csv"
        self.data = pd.read_csv(self.file)
        self.metadata_creator = (DataFrameMetadataCreator(self.data).
                                 compute_advanced_structural_types().
                                 compute_column_kind())
        self.metadata1 = self.metadata_creator.get_metadata()
        self.metadata2 = self.metadata_creator.get_metadata()

    def test_size_compare(self):
        self.compartor.add_comparator_type(SizeComparator())
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata2), 0)
        self.compartor.add_settings(Settings.NO_RATIO)
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata2), 0)

    def test_incomplete_compare(self):
        self.compartor.add_comparator_type(IncompleteColumnsComparator())
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata2), 0)
        self.compartor.add_settings(Settings.NO_RATIO)
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata2), 0)

    def test_exact_names_compare(self):
        self.compartor.add_comparator_type(ColumnExactNamesComparator())
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata2), 0)
        self.compartor.add_settings(Settings.NO_RATIO)
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata2), 0)

    def test_embeddings_names_compare(self):
        self.metadata_creator.compute_column_names_embeddings()
        self.metadata2 = self.metadata_creator.get_metadata()
        self.metadata1 = self.metadata_creator.get_metadata()
        self.compartor.add_comparator_type(ColumnNamesEmbeddingsComparator())

        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata2), 0)
        self.compartor.add_settings(Settings.NO_RATIO)
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata2), 0)

    def test_kind_compare(self):
        self.metadata_creator.compute_column_kind()
        self.metadata2 = self.metadata_creator.get_metadata()
        self.metadata1 = self.metadata_creator.get_metadata()
        self.compartor.add_comparator_type(KindComparator())

        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata2), 0)
        self.compartor.add_settings(Settings.NO_RATIO)
        self.assertEqual(self.compartor.compare(self.metadata1, self.metadata2), 0)

    def test_kind_BOOL_compare(self):
        self.metadata_creator.compute_column_kind()
        metadata2 = self.metadata_creator.get_metadata()
        metadata1 = self.metadata_creator.get_metadata()
        self.assertEqual(self.compartor.add_comparator_type(KindComparator([DataKind.BOOL])).compare(metadata1, metadata2), 0)

    def test_kind_ID_compare(self):
        self.metadata_creator.compute_column_kind()
        metadata2 = self.metadata_creator.get_metadata()
        metadata1 = self.metadata_creator.get_metadata()
        self.assertEqual(self.compartor.add_comparator_type(KindComparator([DataKind.ID])).compare(metadata1, metadata2), 0)

    def test_kind_CATEGORICAL_compare(self):
        self.metadata_creator.compute_column_kind()
        metadata2 = self.metadata_creator.get_metadata()
        metadata1 = self.metadata_creator.get_metadata()
        self.assertEqual(self.compartor.add_comparator_type(KindComparator([DataKind.CATEGORICAL])).compare(metadata1, metadata2), 0)

    def test_kind_CONSTANT_compare(self):
        self.metadata_creator.compute_column_kind()
        metadata2 = self.metadata_creator.get_metadata()
        metadata1 = self.metadata_creator.get_metadata()
        self.assertEqual(self.compartor.add_comparator_type(KindComparator([DataKind.CONSTANT])).compare(metadata1, metadata2), 0)

if __name__ == '__main__':
    unittest.main()
