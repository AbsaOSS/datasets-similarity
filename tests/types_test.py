import unittest

import pandas as pd

from similarity.Types import is_id, is_numerical, is_bool, get_data_kind, DataKind, is_constant, is_int, is_human_gen


class TestID(unittest.TestCase):
    def setUp(self):
        self.directory = "../data/"
        self.directory_val = "../data_validation/"

    def control_test_for_columns(self, data: pd.DataFrame, id_column: str):
        for i in data.columns:
            if i != id_column:
                self.assertFalse(is_id(data[i]))

    def test_aircraft(self):
        data = pd.read_csv(self.directory + "aircraft-data_nov_dec.csv")
        self.assertTrue(is_id(data["Unnamed: 0"]))
        self.control_test_for_columns(data, "Unnamed: 0")

    def test_netflix(self):
        data = pd.read_csv(self.directory + "netflix_titles.csv")
        self.assertTrue(is_id(data["show_id"]))

    def test_wine(self):
        data = pd.read_csv(self.directory_val + "winequality.csv")
        self.control_test_for_columns(data, "")

class TestEdgeCasesNumerical(unittest.TestCase):
    def setUp(self):
        self.file = "../data_validation/edge_cases.csv"
        self.data = pd.read_csv(self.file)
        data = {'int_str': ['2', '3', '5', '2'],
                'float_str': ['2.2', '3.1', '5.3', '2.2'],
                'float_but_int_str': ['2.0', '3.0', '5.0', '2.0'],
                'float_with_nan': ['NaN', '3.0', 'Nan', '2.0'],
                'float_with_minus': ['-2.1', '-3.0', '5.0', '2.0'],

                'float_computer_gen': ['-2.12341', '-3.02305', '5.234865', '2.345624'],
                'float_rounded': ['-2.25', '-3.3355', '5.24', '2.445'],
                }
        self.str_data = pd.DataFrame(data)

    def test_numeric(self):
        self.assertTrue(is_numerical(self.data["id_column"]))
        self.assertTrue(is_numerical(self.data["number_int"]))
        self.assertTrue(is_numerical(self.data["number_float"]))
        self.assertTrue(is_numerical(self.data["float_but_int"]))
        self.assertTrue(is_numerical(self.data["bool_int"]))
        self.assertTrue(is_numerical(self.data["constant_number"]))

        self.assertFalse(is_numerical(self.data["id_text_column"]))
        self.assertFalse(is_numerical(self.data["id_column_both"]))

    def test_numeric_string(self):
        self.assertTrue(is_numerical(self.data["number_int_str"]))
        self.assertTrue(is_numerical(self.data["number_float_str"]))
        self.assertTrue(is_numerical(self.str_data["int_str"]))
        self.assertTrue(is_numerical(self.str_data["float_str"]))
        self.assertTrue(is_numerical(self.str_data["float_but_int_str"]))
        self.assertTrue(is_numerical(self.data["float_str_comma"]))
        self.assertTrue(is_numerical(self.str_data["float_with_nan"]))
        self.assertTrue(is_numerical(self.str_data["float_with_minus"]))
        self.assertTrue(is_numerical(self.str_data["float_computer_gen"]))
        self.assertTrue(is_numerical(self.str_data["float_rounded"]))

    def test_int(self):
        self.assertTrue(is_int(self.data["id_column"]))
        self.assertTrue(is_int(self.data["number_int"]))
        self.assertTrue(is_int(self.data["bool_int"]))
        self.assertTrue(is_int(self.data["constant_number"]))
        self.assertTrue(is_int(self.data["number_int_str"]))
        self.assertTrue(is_int(self.str_data["int_str"]))
        self.assertTrue(is_int(self.data["float_but_int"]))
        self.assertTrue(is_int(self.str_data["float_but_int_str"]))

        self.assertFalse(is_int(self.str_data["float_str"]))
        self.assertFalse(is_int(self.data["number_float_str"]))
        self.assertFalse(is_int(self.data["number_float"]))
        self.assertFalse(is_int(self.data["float_str_comma"]))
        self.assertFalse(is_int(self.str_data["float_with_nan"]))
        self.assertFalse(is_int(self.str_data["float_with_minus"]))
        self.assertFalse(is_int(self.str_data["float_computer_gen"]))
        self.assertFalse(is_int(self.str_data["float_rounded"]))

    def test_float_human_comp(self):
        self.assertTrue(is_human_gen(self.str_data["float_str"]))
        self.assertTrue(is_human_gen(self.data["number_float_str"]))
        self.assertTrue(is_human_gen(self.data["number_float"]))
        self.assertTrue(is_human_gen(self.data["float_str_comma"]))
        self.assertTrue(is_human_gen(self.str_data["float_with_nan"]))
        self.assertTrue(is_human_gen(self.str_data["float_with_minus"]))

        self.assertFalse(is_human_gen(self.str_data["float_computer_gen"]))
        self.assertFalse(is_human_gen(self.str_data["float_rounded"]))

class TestDataKind(unittest.TestCase):
    def setUp(self):
        self.file = "../data_validation/edge_cases.csv"
        self.data = pd.read_csv(self.file)
        file_edge = "../data_validation/edge_cases.csv"
        self.data_edge = pd.read_csv(file_edge)

    def test_id(self):
        self.assertTrue(is_id(self.data["id_column"]))
        self.assertTrue(is_id(self.data["id_text_column"]))
        self.assertEqual(DataKind.ID, get_data_kind(self.data["id_column"]))
        self.assertEqual(DataKind.ID, get_data_kind(self.data["id_text_column"]))
        self.assertTrue(is_id(self.data_edge["id_column"]))
        self.assertTrue(is_id(self.data_edge["id_text_column"]))
        self.assertTrue(is_id(self.data_edge["id_column_both"]))

    def test_bool(self):
        self.assertFalse(is_bool(self.data["id_column"]))

        self.assertTrue(is_bool(self.data["bool_int"]))
        self.assertTrue(is_bool(self.data["bool_str"]))
        self.assertTrue(is_bool(self.data["bool_TF"]))
        self.assertTrue(is_bool(self.data["bool_TFtf"]))

        self.assertEqual(DataKind.BOOL, get_data_kind(self.data["bool_int"]))
        self.assertEqual(DataKind.BOOL, get_data_kind(self.data["bool_str"]))
        self.assertEqual(DataKind.BOOL, get_data_kind(self.data["bool_TF"]))
        self.assertEqual(DataKind.BOOL, get_data_kind(self.data["bool_TFtf"]))

    def test_constant(self):
        self.assertFalse(is_constant(self.data["bool_int"]))

        self.assertTrue(is_constant(self.data["constant_number"]))
        self.assertTrue(is_constant(self.data["constant_str"]))

        self.assertEqual(DataKind.CONSTANT, get_data_kind(self.data["constant_number"]))
        self.assertEqual(DataKind.CONSTANT, get_data_kind(self.data["constant_str"]))
        self.assertEqual(DataKind.UNDEFINED, get_data_kind(self.data["number_int"]))

if __name__ == '__main__':
    unittest.main()
