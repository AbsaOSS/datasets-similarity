import unittest

import pandas as pd

from similarity.DataFrameMetadataCreator import DataFrameMetadataCreator
from similarity.Types import (INT, HUMAN_GENERATED, ALPHABETIC, ALPHANUMERIC, NUMERICAL, NONNUMERICAL)


class TestGetColumnType(unittest.TestCase):
    def setUp(self):
        # database, names = f.load__csv_files_from_folder("../data")
        # metadata: dict[str, DataFrameMetadata] = defaultdict()
        # for dataframe, name in zip(database, names):
        #     metadata[name] = DataFrameMetadataCreator(dataframe).compute_advanced_structural_types().get_metadata()
        self.file = "../data_validation/edge_cases.csv"
        self.data = pd.read_csv(self.file)
        self.metadata = DataFrameMetadataCreator(self.data).compute_advanced_structural_types().get_metadata()

    def test_get_column(self):
        column_names = self.metadata.get_numerical_columns_names()
        self.assertTrue('id_column' in column_names)
        self.assertTrue('number_int' in column_names)
        self.assertTrue('number_int_str' in column_names)
        self.assertTrue('number_float' in column_names)
        self.assertTrue('number_float_str' in column_names)
        self.assertTrue('bool_int' in column_names)
        self.assertTrue('constant_number' in column_names)
        self.assertTrue('float_str_comma' in column_names)

    def test_get_column_type(self):
        self.assertEqual(self.metadata.get_column_type('id_column'), Types.NUMERICAL.value.INT)
        self.assertEqual(self.metadata.get_column_type('bool_str'), Types.NONNUMERICAL.value.TEXT.value.WORD.value.ALPHABETIC)
        self.assertNotEqual(self.metadata.get_column_type('bool_str'), Types.NUMERICAL)
        self.assertNotEqual(self.metadata.get_column_type('bool_str'), Types.NONNUMERICAL.value.TEXT)
        self.assertEqual(self.metadata.get_column_type('id_text_column'), Types.NONNUMERICAL.value.TEXT.value.WORD.value.ALPHABETIC)



if __name__ == '__main__':
    unittest.main()