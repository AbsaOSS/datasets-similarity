import os
import unittest

import pandas as pd

from similarity_framework.src.impl.metadata.type_metadata_creator import TypeMetadataCreator
from similarity_framework.src.models.metadata import MetadataCreatorInput

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class TestGetColumnType(unittest.TestCase):
    def setUp(self):
        # database, names = f.load__csv_files_from_folder("../data")
        # metadata: dict[str, DataFrameMetadata] = defaultdict()
        # for dataframe, name in zip(database, names):
        #     metadata[name] = DataFrameMetadataCreator(dataframe).compute_advanced_structural_types().get_metadata()

        self.file = os.path.join(THIS_DIR, '../data_validation/edge_cases.csv')
        self.data = pd.read_csv(self.file)
        self.metadata_creator = (TypeMetadataCreator().
                                 compute_advanced_structural_types().
                                 compute_column_kind())
        self.metadata = self.metadata_creator.get_metadata(MetadataCreatorInput(dataframe=self.data))

    def test_get_column(self):
        column_names = self.metadata.get_numerical_columns_names()
        self.assertTrue('id_column' in column_names)
        self.assertTrue('number_int' in column_names)
        self.assertTrue('number_int_str' in column_names)
        self.assertTrue('number_float' in column_names)
        self.assertTrue('number_float_str' in column_names)
        self.assertTrue('float_but_int' in column_names)
        self.assertTrue('bool_int' in column_names)
        self.assertTrue('constant_number' in column_names)
        self.assertTrue('float_str_comma' in column_names)

    def test_default_fill(self):
        self.assertEqual(self.metadata.size, 10)

        self.assertTrue('id_column' in self.metadata.column_names)
        self.assertTrue('number_int' in self.metadata.column_names)
        self.assertTrue('number_int_str' in self.metadata.column_names)
        self.assertTrue('number_float' in self.metadata.column_names)
        self.assertTrue('number_float_str' in self.metadata.column_names)
        self.assertTrue('float_but_int' in self.metadata.column_names)
        self.assertTrue('bool_int' in self.metadata.column_names)
        self.assertTrue('constant_number' in self.metadata.column_names)
        self.assertTrue('float_str_comma' in self.metadata.column_names)

        self.assertTrue('id column' in self.metadata.column_names_clean.values())
        self.assertTrue('number int' in self.metadata.column_names_clean.values())
        self.assertTrue('number int str' in self.metadata.column_names_clean.values())
        self.assertTrue('number float' in self.metadata.column_names_clean.values())
        self.assertTrue('number float str' in self.metadata.column_names_clean.values())
        self.assertTrue('float but int' in self.metadata.column_names_clean.values())
        self.assertTrue('bool int' in self.metadata.column_names_clean.values())
        self.assertTrue('constant number' in self.metadata.column_names_clean.values())
        self.assertTrue('float str comma' in self.metadata.column_names_clean.values())

        self.assertEqual(sum(1 for value in self.metadata.column_incomplete.values() if value),
                         0)  # any incomplete column
        data = {'int_str': ['2', '3', '5', '2'],
                'float_str': ['2.2', '3.1', '5.3', '2.2'],
                'float_but_int_str': ['2.0', '3.0', '5.0', '2.0'],
                'float_with_nan': ['NaN', '3.1', 'Nan', '2.3'],
                'float_with_minus': ['-2.1', '-3.0', '5.0', '2.0']}
        str_data = pd.DataFrame(data)
        str_data.float_with_nan = str_data.float_with_nan.astype(float)
        metadata_creator = TypeMetadataCreator().compute_incomplete_column()
        metadata = metadata_creator.get_metadata(MetadataCreatorInput(dataframe=str_data))
        self.assertEqual(sum(1 for value in metadata.column_incomplete.values() if value),
                         1)  # any incomplete column

        # todo correlated columns

    def test_metadata_type_column(self):
        self.assertTrue('id_column' in self.metadata.numerical_metadata)
        self.assertTrue('number_int' in self.metadata.numerical_metadata)
        self.assertTrue('number_int_str' in self.metadata.numerical_metadata)
        self.assertTrue('number_float' in self.metadata.numerical_metadata)
        self.assertTrue('number_float_str' in self.metadata.numerical_metadata)
        self.assertTrue('float_but_int' in self.metadata.numerical_metadata)
        self.assertTrue('bool_int' in self.metadata.numerical_metadata)
        self.assertTrue('constant_number' in self.metadata.numerical_metadata)
        self.assertTrue('float_str_comma' in self.metadata.numerical_metadata)

        self.assertFalse('id_column' in self.metadata.nonnumerical_metadata)
        self.assertFalse('number_int' in self.metadata.nonnumerical_metadata)
        self.assertFalse('number_int_str' in self.metadata.nonnumerical_metadata)
        self.assertFalse('number_float' in self.metadata.nonnumerical_metadata)
        self.assertFalse('number_float_str' in self.metadata.nonnumerical_metadata)
        self.assertFalse('float_but_int' in self.metadata.nonnumerical_metadata)
        self.assertFalse('bool_int' in self.metadata.nonnumerical_metadata)
        self.assertFalse('constant_number' in self.metadata.nonnumerical_metadata)
        self.assertFalse('float_str_comma' in self.metadata.nonnumerical_metadata)

        self.assertTrue('id_text_column' in self.metadata.nonnumerical_metadata)
        self.assertTrue('id_column_both' in self.metadata.nonnumerical_metadata)
        self.assertTrue('bool_str' in self.metadata.nonnumerical_metadata)
        self.assertTrue('bool_TF' in self.metadata.nonnumerical_metadata)
        self.assertTrue('bool_TFtf' in self.metadata.nonnumerical_metadata)
        self.assertTrue('constant_str' in self.metadata.nonnumerical_metadata)

        self.assertFalse('id_text_column' in self.metadata.numerical_metadata)
        self.assertFalse('id_column_both' in self.metadata.numerical_metadata)
        self.assertFalse('bool_str' in self.metadata.numerical_metadata)
        self.assertFalse('bool_TF' in self.metadata.numerical_metadata)
        self.assertFalse('bool_TFtf' in self.metadata.numerical_metadata)
        self.assertFalse('constant_str' in self.metadata.numerical_metadata)

        # numerical metadata
        self.assertTrue(self.metadata.numerical_metadata['number_int'].max_value, 8)
        self.assertTrue(self.metadata.numerical_metadata['number_int'].min_value, 1)
        self.assertTrue(self.metadata.numerical_metadata['number_int'].range_size, 7)
        self.assertTrue(self.metadata.numerical_metadata['number_int'].same_value_length, True)

        # nonnumerical metadata
        self.assertTrue(self.metadata.nonnumerical_metadata['bool_str'].longest, "WOMAN")
        self.assertTrue(self.metadata.nonnumerical_metadata['bool_str'].shortest, "MAN")
        self.assertTrue(self.metadata.nonnumerical_metadata['bool_str'].avg_length, 5)

    def test_metadata_kind_column(self):
        self.assertTrue('id_column' in self.metadata.kind_metadata)
        self.assertTrue('number_int' in self.metadata.kind_metadata)
        self.assertTrue('number_int_str' in self.metadata.kind_metadata)
        self.assertTrue('number_float' in self.metadata.kind_metadata)
        self.assertTrue('number_float_str' in self.metadata.kind_metadata)
        self.assertTrue('float_but_int' in self.metadata.kind_metadata)
        self.assertTrue('bool_int' in self.metadata.kind_metadata)
        self.assertTrue('constant_number' in self.metadata.kind_metadata)
        self.assertTrue('float_str_comma' in self.metadata.kind_metadata)

        self.assertTrue('id_text_column' in self.metadata.kind_metadata)
        self.assertTrue('id_column_both' in self.metadata.kind_metadata)
        self.assertTrue('bool_str' in self.metadata.kind_metadata)
        self.assertTrue('bool_TF' in self.metadata.kind_metadata)
        self.assertTrue('bool_TFtf' in self.metadata.kind_metadata)
        self.assertTrue('constant_str' in self.metadata.kind_metadata)

        self.assertEqual(self.metadata.categorical_metadata, {})

        # id metadata
        self.assertTrue(self.metadata.kind_metadata['id_column_both'].longest, "AB1")
        self.assertTrue(self.metadata.kind_metadata['id_column_both'].shortest, "AB1")
        self.assertFalse(self.metadata.kind_metadata['id_column_both'].nulls)
        self.assertTrue(self.metadata.kind_metadata['id_column_both'].ratio_max_length, 3 / 10)

        self.assertTrue(self.metadata.kind_metadata['id_column'].longest, 10)
        self.assertTrue(self.metadata.kind_metadata['id_column'].shortest, 1)
        self.assertFalse(self.metadata.kind_metadata['id_column'].nulls)
        self.assertTrue(self.metadata.kind_metadata['id_column'].ratio_max_length, 2 / 10)

        # constant metadata
        self.assertTrue(self.metadata.kind_metadata['constant_str'].value, tuple["MA"])
        self.assertIsNone(self.metadata.kind_metadata['constant_str'].distribution)
        self.assertFalse(self.metadata.kind_metadata['constant_str'].nulls)

        self.assertTrue(self.metadata.kind_metadata['constant_number'].value, tuple[1])
        self.assertIsNone(self.metadata.kind_metadata['constant_number'].distribution)
        self.assertFalse(self.metadata.kind_metadata['constant_number'].nulls)

        # bool metadata
        self.assertTrue(self.metadata.kind_metadata['bool_str'].value, tuple["WOMAN", "MAN"])
        self.assertTrue(self.metadata.kind_metadata['bool_str'].distribution, tuple[6, 4])
        self.assertFalse(self.metadata.kind_metadata['bool_str'].nulls)

    def test_embeddings(self):
        self.assertEqual(self.metadata.column_embeddings, {})
        self.assertEqual(self.metadata.column_name_embeddings, {})
        self.assertIsNot(self.metadata.column_names_clean.values(), {})
        self.assertIsNot(self.metadata.column_names, {})

        metadata = (self.metadata_creator.compute_column_names_embeddings()
                    .compute_column_embeddings().get_metadata(MetadataCreatorInput(dataframe=self.data)))

        self.assertIsNot({}, metadata.column_embeddings)
        self.assertIsNot({}, metadata.column_name_embeddings)
        self.assertIsNot({}, metadata.column_names_clean.values())
        self.assertIsNot({}, metadata.column_names)


if __name__ == '__main__':
    unittest.main()
