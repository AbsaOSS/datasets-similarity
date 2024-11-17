import os
import unittest

import pandas as pd

from src.impl.types_functions import is_id, is_numerical, is_bool, get_data_kind, DataKind, is_constant, is_int, is_human_gen, \
    is_not_numerical, is_categorical, is_word, is_phrase, is_sentence, is_article, is_multiple, is_date, \
    is_true_multiple, get_basic_type, get_advanced_type, is_alphabetic_word, is_alphanumeric_word, \
    get_advanced_structural_type, series_to_numeric
from src.models.types_ import NUMERICAL, NONNUMERICAL, DATE, ALPHABETIC, ALL, ALPHANUMERIC, \
    MULTIPLE_VALUES, PHRASE, SENTENCE, ARTICLE, INT, FLOAT, HUMAN_GENERATED, COMPUTER_GENERATED, UNDEFINED, WORD

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class TestID(unittest.TestCase):
    def setUp(self):
        self.directory = os.path.join(THIS_DIR, 'data/')
        self.directory_val = os.path.join(THIS_DIR, 'data_validation/')

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
        self.file = os.path.join(THIS_DIR, 'data_validation/edge_cases.csv')
        self.data = pd.read_csv(self.file)
        data = {'int_str': ['2', '3', '5', '2'],
                'float_str': ['2.2', '3.1', '5.3', '2.2'],
                'float_but_int_str': ['2.0', '3.0', '5.0', '2.0'],
                'float_with_nan': ['NaN', '3.2', 'Nan', '2.3'],
                'float_with_minus': ['-2.1', '-3.0', '5.0', '2.0'],

                'float_computer_gen': ['-2.12341', '-3.02305', '5.234865', '2.345624'],
                'float_rounded': ['-2.25', '-3.3355', '5.24', '2.445'],
                }
        self.str_data = pd.DataFrame(data)

    def test_numeric(self):
        self.assertTrue(is_numerical(series_to_numeric(self.data["id_column"])))
        self.assertTrue(is_numerical(series_to_numeric(self.data["number_int"])))
        self.assertTrue(is_numerical(series_to_numeric(self.data["number_float"])))
        self.assertTrue(is_numerical(series_to_numeric(self.data["float_but_int"])))
        self.assertTrue(is_numerical(series_to_numeric(self.data["bool_int"])))
        self.assertTrue(is_numerical(series_to_numeric(self.data["constant_number"])))

        self.assertFalse(is_numerical(series_to_numeric(self.data["id_text_column"])))
        self.assertFalse(is_numerical(series_to_numeric(self.data["id_column_both"])))
        self.assertFalse(is_numerical(series_to_numeric(self.data["bool_str"])))
        self.assertFalse(is_numerical(series_to_numeric(self.data["bool_TF"])))
        self.assertFalse(is_numerical(series_to_numeric(self.data["bool_TFtf"])))
        self.assertFalse(is_numerical(series_to_numeric(self.data["constant_str"])))

    def test_numeric_string(self):
        self.assertTrue(is_numerical(series_to_numeric(self.data["number_int_str"])))
        self.assertTrue(is_numerical(series_to_numeric(self.data["number_float_str"])))
        self.assertTrue(is_numerical(series_to_numeric(self.str_data["int_str"])))
        self.assertTrue(is_numerical(series_to_numeric(self.str_data["float_str"])))
        self.assertTrue(is_numerical(series_to_numeric(self.str_data["float_but_int_str"])))
        self.assertTrue(is_numerical(series_to_numeric(self.data["float_str_comma"])))
        self.assertTrue(is_numerical(series_to_numeric(self.str_data["float_with_nan"])))
        self.assertTrue(is_numerical(series_to_numeric(self.str_data["float_with_minus"])))
        self.assertTrue(is_numerical(series_to_numeric(self.str_data["float_computer_gen"])))
        self.assertTrue(is_numerical(series_to_numeric(self.str_data["float_rounded"])))

    def test_int(self):
        self.assertTrue(is_int(self.data["id_column"]))
        self.assertTrue(is_int(self.data["number_int"]))
        self.assertTrue(is_int(self.data["bool_int"]))
        self.assertTrue(is_int(self.data["constant_number"]))
        self.assertTrue(is_int(self.data["number_int_str"]))
        self.assertTrue(is_int(series_to_numeric(self.str_data["int_str"])))
        self.assertTrue(is_int(self.data["float_but_int"]))
        self.assertTrue(is_int(series_to_numeric(self.str_data["float_but_int_str"])))

        self.assertFalse(is_int(series_to_numeric(self.str_data["float_str"])))
        self.assertFalse(is_int(series_to_numeric(self.data["number_float_str"])))
        self.assertFalse(is_int(self.data["number_float"]))
        self.assertFalse(is_int(series_to_numeric(self.data["float_str_comma"])))
        self.assertFalse(is_int(series_to_numeric(self.str_data["float_with_nan"])))
        self.assertFalse(is_int(series_to_numeric(self.str_data["float_with_minus"])))
        self.assertFalse(is_int(series_to_numeric(self.str_data["float_computer_gen"])))
        self.assertFalse(is_int(series_to_numeric(self.str_data["float_rounded"])))

    def test_float_human_comp(self):
        self.assertTrue(is_human_gen(self.str_data["float_str"]))
        self.assertTrue(is_human_gen(self.data["number_float_str"]))
        self.assertTrue(is_human_gen(self.data["number_float"]))
        self.assertTrue(is_human_gen(self.data["float_str_comma"]))
        self.assertTrue(is_human_gen(self.str_data["float_with_nan"]))
        self.assertTrue(is_human_gen(self.str_data["float_with_minus"]))

        self.assertFalse(is_human_gen(self.str_data["float_computer_gen"]))
        self.assertFalse(is_human_gen(self.str_data["float_rounded"]))


class TestNonNumerical(unittest.TestCase):
    def setUp(self):
        self.file = os.path.join(THIS_DIR, 'data_validation/edge_cases.csv')
        self.data = pd.read_csv(self.file)
        data = {'int_str': ['2', '3', '5', '2'],
                'float_with_nan': ['NaN', '3.1', 'Nan', '2.2'],
                'float_with_minus': ['-2.1', '-3.0', '5.0', '2.0'],
                'TFtf': ['true', 'false', 'True', 'False'],
                }
        self.str_data = pd.DataFrame(data)

    def test_not_numeric(self):
        self.assertTrue(is_not_numerical(self.data["id_text_column"]))
        self.assertTrue(is_not_numerical(self.data["id_column_both"]))
        self.assertTrue(is_not_numerical(self.data["bool_str"]))
        # self.assertTrue(is_not_numerical(self.data["bool_TF"]))
        self.assertTrue(is_not_numerical(self.str_data["TFtf"]))
        self.assertTrue(is_not_numerical(self.data["constant_str"]))

        self.assertFalse(is_not_numerical(series_to_numeric(self.data["float_str_comma"])))
        self.assertFalse(is_not_numerical(self.data["constant_number"]))
        self.assertFalse(is_not_numerical(self.data["bool_int"]))
        self.assertFalse(is_not_numerical(self.data["number_float"]))
        self.assertFalse(is_not_numerical(self.data["number_float_str"]))
        self.assertFalse(is_not_numerical(self.data["float_but_int"]))
        self.assertFalse(is_not_numerical(self.data["number_int"]))
        self.assertFalse(is_not_numerical(self.data["number_int_str"]))
        self.assertFalse(is_not_numerical(self.data["id_column"]))
        self.assertFalse(is_not_numerical(series_to_numeric(self.str_data["int_str"])))
        self.assertFalse(is_not_numerical(series_to_numeric(self.str_data["float_with_nan"])))
        self.assertFalse(is_not_numerical(series_to_numeric(self.str_data["float_with_minus"])))

    def test_string_type(self):
        data = {
            'word_aZ': ['Pepa', 'Matej', 'Tomas', 'marcel'],
            'word_aZ09': ['AB09', 'McA2', 'MoA3', '223A'],
            'word_all': ['AB-09', 'McA2', 'Mo/A3', '223-A'],
            'phrase': ['John Doe', 'Max Mo', 'No oj', 'La lu li'],
            'sentence': ['Gregory, on my word we’ll not carry coals.', 'No, for then we should be colliers.',
                         'I mean, an we be in choler, we’ll draw.', 'Ay, while you live, draw your neck out of '
                                                                    'collar.'],
            'article': ['Two households, both alike in dignity (In fair Verona, where we lay our scene), From ancient '
                        'grudge break to new mutiny,Where civil blood makes civil hands unclean. From forth the fatal '
                        'loins of these two foes A pair of star-crossed lovers take their life.',

                        'Whose misadventured piteous overthrows Doth with their death bury their parents’ strife.The '
                        'fearful passage of their death-marked love And the continuance of their parents’ rage',
                        'Which, but their children’s end, naught could remove, Is now the two hours’ traffic of our '
                        'stage;',

                        'The which, if you with patient ears attend, What here shall miss, our toil shall strive to '
                        'mend.'],
            'multiple': ['Milk, chocolate, flour', 'milk, bread, butter, salt', 'flour, milk', 'chocolate'],
            'multiple-': ['Milk - chocolate - flour', 'milk - bread - butter - salt', 'flour - milk', 'chocolate - '
                                                                                                      'orange - '
                                                                                                      'whisky'],
            'multiple;': ['Milk; chocolate; flour', 'milk; bread; butter; salt', 'flour; milk', 'chocolate; orange; '
                                                                                                'whisky'],
            'multiple|': ['Milk|chocolate|flour', 'milk|bread|butter|salt', 'flour|milk', 'chocolate|orange|whisky'],

        }
        df_data = pd.DataFrame(data)
        self.assertTrue(is_not_numerical(df_data["word_aZ"]))
        self.assertTrue(is_not_numerical(df_data["word_aZ09"]))
        self.assertTrue(is_not_numerical(df_data["word_all"]))
        self.assertTrue(is_not_numerical(df_data["phrase"]))
        self.assertTrue(is_not_numerical(df_data["sentence"]))
        self.assertTrue(is_not_numerical(df_data["article"]))
        self.assertTrue(is_not_numerical(df_data["multiple"]))
        self.assertTrue(is_not_numerical(df_data["multiple-"]))
        self.assertTrue(is_not_numerical(df_data["multiple;"]))
        self.assertTrue(is_not_numerical(df_data["multiple|"]))

        self.assertFalse(is_categorical(df_data["word_aZ"]))
        self.assertFalse(is_categorical(df_data["word_aZ09"]))
        self.assertFalse(is_categorical(df_data["word_all"]))
        self.assertFalse(is_categorical(df_data["phrase"]))
        self.assertFalse(is_categorical(df_data["sentence"]))
        self.assertFalse(is_categorical(df_data["article"]))
        self.assertFalse(is_categorical(df_data["multiple"]))
        self.assertFalse(is_categorical(df_data["multiple-"]))
        self.assertFalse(is_categorical(df_data["multiple;"]))
        self.assertFalse(is_categorical(df_data["multiple|"]))

        self.assertTrue(is_word(df_data["word_aZ"]))
        self.assertTrue(is_word(df_data["word_aZ09"]))
        self.assertTrue(is_word(df_data["word_all"]))
        self.assertTrue(is_alphabetic_word(df_data["word_aZ"]))
        self.assertTrue(is_alphanumeric_word(df_data["word_aZ09"]))
        self.assertFalse(is_alphabetic_word(df_data["word_all"]))
        self.assertFalse(is_alphanumeric_word(df_data["word_all"]))
        self.assertTrue(is_phrase(df_data["phrase"]))
        self.assertTrue(is_sentence(df_data["sentence"]))
        self.assertTrue(is_multiple(df_data["multiple"]))
        self.assertTrue(is_multiple(df_data["multiple-"]))
        self.assertTrue(is_multiple(df_data["multiple;"]))
        self.assertTrue(is_multiple(df_data["multiple|"]))
        self.assertTrue(is_true_multiple(df_data["multiple"]))
        self.assertTrue(is_true_multiple(df_data["multiple-"]))
        self.assertTrue(is_true_multiple(df_data["multiple;"]))
        self.assertTrue(is_true_multiple(df_data["multiple|"]))
        self.assertTrue(is_article(df_data["article"]))

    def test_categorical_type(self):
        data = {
            'ordinal': ['big', 'small', 'medium', 'small', 'big', 'small', 'medium', 'medium', 'medium', 'small', 'big',
                        'small', 'medium', 'small', 'big', 'small', 'medium', 'medium', 'medium', 'small'],
            'ordinal_grades': ['A', 'A', 'B', 'B', 'F', 'A', 'C', 'A', 'D', 'A', 'A', 'A', 'B', 'B', 'F', 'A', 'C', 'A',
                               'D', 'A'],
            'ordinal_class': ['middle class', 'middle class', 'rich', 'poor', 'rich', 'poor', 'poor', 'middle class',
                              'poor', 'poor', 'middle class', 'middle class', 'rich', 'poor', 'rich', 'poor', 'poor',
                              'middle class', 'poor', 'poor'],
            'nominal': ['car', 'house', 'garden', 'garden', 'garden', 'car', 'house', 'garden', 'house', 'garden',
                        'car', 'house', 'garden', 'garden', 'garden', 'car', 'house', 'garden', 'house', 'garden'],
            'nominal_blood_type': ['A', 'AB', 'A', 'B', '0', 'A', 'AB', '0', 'A', '0', 'A', 'AB', 'A', 'B', '0', 'A',
                                   'AB', '0', 'A', '0'],
        }
        df_data = pd.DataFrame(data)
        self.assertTrue(is_not_numerical(df_data["ordinal"]))
        self.assertTrue(is_not_numerical(df_data["ordinal_grades"]))
        self.assertTrue(is_not_numerical(df_data["ordinal_class"]))
        self.assertTrue(is_not_numerical(df_data["nominal"]))
        self.assertTrue(is_not_numerical(df_data["nominal_blood_type"]))

        self.assertTrue(is_categorical(df_data["ordinal"]))
        self.assertTrue(is_categorical(df_data["ordinal_grades"]))
        self.assertTrue(is_categorical(df_data["ordinal_class"]))
        self.assertTrue(is_categorical(df_data["nominal"]))
        self.assertTrue(is_categorical(df_data["nominal_blood_type"]))

        # todo
        # self.assertTrue(is_ordinal(df_data["ordinal"]))
        # self.assertTrue(is_ordinal(df_data["ordinal_grades"]))
        # self.assertTrue(is_ordinal(df_data["ordinal_class"]))
        # self.assertTrue(is_nominal(df_data["nominal"]))
        # self.assertTrue(is_nominal(df_data["nominal_blood_type"]))


class TestDataKind(unittest.TestCase):
    def setUp(self):
        self.file = os.path.join(THIS_DIR, 'data_validation/edge_cases.csv')
        self.data = pd.read_csv(self.file)
        file_edge = os.path.join(THIS_DIR, 'data_validation/edge_cases.csv')
        self.data_edge = pd.read_csv(file_edge)

        data = {'TFtf': ['true', 'false', 'true', 'False', 'True'],
                }
        data_categorical = {
            'ordinal': ['big', 'small', 'medium', 'small', 'big', 'small', 'medium', 'medium', 'medium', 'small', 'big',
                        'small', 'medium', 'small', 'big', 'small', 'medium', 'medium', 'medium', 'small'],
            'ordinal_grades': ['A', 'A', 'B', 'B', 'F', 'A', 'C', 'A', 'D', 'A', 'A', 'A', 'B', 'B', 'F', 'A', 'C', 'A',
                               'D', 'A'],
            'ordinal_class': ['middle class', 'middle class', 'rich', 'poor', 'rich', 'poor', 'poor', 'middle class',
                              'poor', 'poor', 'middle class', 'middle class', 'rich', 'poor', 'rich', 'poor', 'poor',
                              'middle class', 'poor', 'poor'],
            'nominal': ['car', 'house', 'garden', 'garden', 'garden', 'car', 'house', 'garden', 'house', 'garden',
                        'car', 'house', 'garden', 'garden', 'garden', 'car', 'house', 'garden', 'house', 'garden'],
            'nominal_blood_type': ['A', 'AB', 'A', 'B', '0', 'A', 'AB', '0', 'A', '0', 'A', 'AB', 'A', 'B', '0', 'A',
                                   'AB', '0', 'A', '0'],
        }
        self.categorical_data = pd.DataFrame(data_categorical)
        self.str_data = pd.DataFrame(data)

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
        self.assertTrue(is_bool(self.str_data["TFtf"]))

        self.assertEqual(DataKind.BOOL, get_data_kind(self.data["bool_int"]))
        self.assertEqual(DataKind.BOOL, get_data_kind(self.data["bool_str"]))
        self.assertEqual(DataKind.BOOL, get_data_kind(self.data["bool_TF"]))
        self.assertEqual(DataKind.BOOL, get_data_kind(self.data["bool_TFtf"]))
        self.assertEqual(DataKind.BOOL, get_data_kind(self.str_data["TFtf"]))

    def test_constant(self):
        self.assertFalse(is_constant(self.data["bool_int"]))

        self.assertTrue(is_constant(self.data["constant_number"]))
        self.assertTrue(is_constant(self.data["constant_str"]))

        self.assertEqual(DataKind.CONSTANT, get_data_kind(self.data["constant_number"]))
        self.assertEqual(DataKind.CONSTANT, get_data_kind(self.data["constant_str"]))
        self.assertEqual(DataKind.UNDEFINED, get_data_kind(self.data["number_int"]))

    def test_categorical(self):
        self.assertEqual(DataKind.CATEGORICAL, get_data_kind(self.categorical_data["ordinal"]))
        self.assertEqual(DataKind.CATEGORICAL, get_data_kind(self.categorical_data["ordinal_grades"]))
        self.assertEqual(DataKind.CATEGORICAL, get_data_kind(self.categorical_data["ordinal_class"]))
        self.assertEqual(DataKind.CATEGORICAL, get_data_kind(self.categorical_data["nominal"]))
        self.assertEqual(DataKind.CATEGORICAL, get_data_kind(self.categorical_data["nominal_blood_type"]))


class TestDataType(unittest.TestCase):
    def setUp(self):
        self.file = os.path.join(THIS_DIR, 'data_validation/edge_cases.csv')
        self.data = pd.read_csv(self.file)
        data = {'int_str': ['2', '3', '5', '2'],
                'float_str': ['2.2', '3.1', '5.3', '2.2'],
                'float_but_int_str': ['2.0', '3.0', '5.0', '2.0'],
                'float_with_nan': ['NaN', '3.1', 'Nan', '2.3'],
                'float_with_minus': ['-2.1', '-3.0', '5.0', '2.0'],

                'float_computer_gen': ['-2.12341', '-3.02305', '5.234865', '2.345624'],
                'float_rounded': ['-2.25', '-3.3355', '5.24', '2.445'],
                'TFtf': ['true', 'false', 'True', 'False'],
                'multiple': ['Milk, chocolate, flour', 'milk, bread, butter, salt', 'flour, milk', 'chocolate'],
                'word_all': ['AB-09', 'McA2', 'Mo/A3', '223-A'],
                'phrase': ['John Doe', 'Max Mo', 'No oj', 'La lu li'],
                'sentence': ['Gregory, on my word we’ll not carry coals.', 'No, for then we should be colliers.',
                             'I mean, an we be in choler, we’ll draw.', 'Ay, while you live, draw your neck out of '
                                                                        'collar.'],
                'article': [
                    'Two households, both alike in dignity (In fair Verona, where we lay our scene), From ancient '
                    'grudge break to new mutiny,Where civil blood makes civil hands unclean. From forth the fatal '
                    'loins of these two foes A pair of star-crossed lovers take their life.',

                    'Whose misadventured piteous overthrows Doth with their death bury their parents’ strife.The '
                    'fearful passage of their death-marked love And the continuance of their parents’ rage',
                    'Which, but their children’s end, naught could remove, Is now the two hours’ traffic of our '
                    'stage;',

                    'The which, if you with patient ears attend, What here shall miss, our toil shall strive to '
                    'mend.'],
                'MM.DD.YYYY': ['11.4.1999', '12.31.1999', '1.3.1999', '11.4.1999'],
                'DDMonYYYY': ['4Feb1999', '31Jan 1999', '3 Nov 1999', '3 Nov 1999']
                }
        self.str_data = pd.DataFrame(data)

    def test_get_basic_type(self):
        self.assertEqual(NUMERICAL, get_basic_type(self.str_data["int_str"]))
        self.assertEqual(NUMERICAL, get_basic_type(self.str_data["float_but_int_str"]))
        self.assertEqual(NUMERICAL, get_basic_type(self.data["bool_int"]))
        self.assertEqual(NUMERICAL, get_basic_type(self.data["constant_number"]))
        self.assertEqual(NUMERICAL, get_basic_type(self.data["id_column"]))
        self.assertEqual(NUMERICAL, get_basic_type(self.data["number_int"]))

        self.assertEqual(NUMERICAL, get_basic_type(self.str_data["float_str"]))
        self.assertEqual(NUMERICAL, get_basic_type(self.str_data["float_with_nan"]))
        self.assertEqual(NUMERICAL, get_basic_type(self.str_data["float_with_minus"]))
        self.assertEqual(NUMERICAL, get_basic_type(self.str_data["float_computer_gen"]))
        self.assertEqual(NUMERICAL, get_basic_type(self.str_data["float_rounded"]))

        self.assertEqual(NONNUMERICAL, get_basic_type(self.data["bool_TF"]))
        self.assertEqual(NONNUMERICAL, get_basic_type(self.data["bool_TFtf"]))

        self.assertEqual(NONNUMERICAL, get_basic_type(self.str_data["TFtf"]))
        self.assertEqual(NONNUMERICAL, get_basic_type(self.data["bool_str"]))
        self.assertEqual(NONNUMERICAL, get_basic_type(self.data["constant_str"]))
        self.assertEqual(NONNUMERICAL, get_basic_type(self.data["id_text_column"]))
        self.assertEqual(NONNUMERICAL, get_basic_type(self.str_data["word_all"]))
        self.assertEqual(NONNUMERICAL, get_basic_type(self.data["id_column_both"]))
        self.assertEqual(NONNUMERICAL, get_basic_type(self.str_data["multiple"]))
        self.assertEqual(NONNUMERICAL, get_basic_type(self.str_data["sentence"]))
        self.assertEqual(NONNUMERICAL, get_basic_type(self.str_data["article"]))

        self.assertEqual(DATE, get_basic_type(self.str_data["MM.DD.YYYY"]))
        self.assertEqual(DATE, get_basic_type(self.str_data["DDMonYYYY"]))

    def test_get_advanced_type(self):
        self.assertEqual(INT, get_advanced_type(self.str_data["int_str"]))
        self.assertEqual(INT, get_advanced_type(self.str_data["float_but_int_str"]))
        self.assertEqual(INT, get_advanced_type(self.data["bool_int"]))
        self.assertEqual(INT, get_advanced_type(self.data["constant_number"]))
        self.assertEqual(INT, get_advanced_type(self.data["id_column"]))
        self.assertEqual(INT, get_advanced_type(self.data["number_int"]))

        self.assertEqual(FLOAT, get_advanced_type(self.str_data["float_str"]))
        self.assertEqual(FLOAT, get_advanced_type(self.str_data["float_with_nan"]))
        self.assertEqual(FLOAT, get_advanced_type(self.str_data["float_with_minus"]))
        self.assertEqual(FLOAT, get_advanced_type(self.str_data["float_computer_gen"]))
        self.assertEqual(FLOAT, get_advanced_type(self.str_data["float_rounded"]))

        self.assertEqual(NONNUMERICAL, get_advanced_type(self.data["bool_TF"]))
        self.assertEqual(NONNUMERICAL, get_advanced_type(self.data["bool_TFtf"]))

        self.assertEqual(NONNUMERICAL, get_advanced_type(self.str_data["TFtf"]))
        self.assertEqual(NONNUMERICAL, get_advanced_type(self.data["bool_str"]))
        self.assertEqual(NONNUMERICAL, get_advanced_type(self.data["constant_str"]))
        self.assertEqual(NONNUMERICAL, get_advanced_type(self.data["id_text_column"]))
        self.assertEqual(NONNUMERICAL, get_advanced_type(self.str_data["word_all"]))
        self.assertEqual(NONNUMERICAL, get_advanced_type(self.data["id_column_both"]))
        self.assertEqual(NONNUMERICAL, get_advanced_type(self.str_data["multiple"]))
        self.assertEqual(NONNUMERICAL, get_advanced_type(self.str_data["sentence"]))
        self.assertEqual(NONNUMERICAL, get_advanced_type(self.str_data["article"]))

        self.assertEqual(DATE, get_advanced_type(self.str_data["MM.DD.YYYY"]))
        self.assertEqual(DATE, get_advanced_type(self.str_data["DDMonYYYY"]))

    def test_get_advanced_structural_type(self):
        self.assertEqual(INT, get_advanced_structural_type(self.str_data["int_str"]))
        self.assertEqual(INT, get_advanced_structural_type(self.str_data["float_but_int_str"]))
        self.assertEqual(INT, get_advanced_structural_type(self.data["bool_int"]))
        self.assertEqual(INT, get_advanced_structural_type(self.data["constant_number"]))
        self.assertEqual(INT, get_advanced_structural_type(self.data["id_column"]))
        self.assertEqual(INT, get_advanced_structural_type(self.data["number_int"]))

        self.assertEqual(HUMAN_GENERATED,
                         get_advanced_structural_type(self.str_data["float_str"]))
        self.assertEqual(HUMAN_GENERATED,
                         get_advanced_structural_type(self.str_data["float_with_nan"]))
        self.assertEqual(HUMAN_GENERATED,
                         get_advanced_structural_type(self.str_data["float_with_minus"]))
        self.assertEqual(COMPUTER_GENERATED,
                         get_advanced_structural_type(self.str_data["float_computer_gen"]))
        self.assertEqual(COMPUTER_GENERATED,
                         get_advanced_structural_type(self.str_data["float_rounded"]))

        self.assertEqual(ALPHABETIC,
                         get_advanced_structural_type(self.data["bool_TF"]))
        self.assertEqual(ALPHABETIC,
                         get_advanced_structural_type(self.data["bool_TFtf"]))

        self.assertEqual(ALPHABETIC,
                         get_advanced_structural_type(self.str_data["TFtf"]))
        self.assertEqual(ALPHABETIC,
                         get_advanced_structural_type(self.data["bool_str"]))
        self.assertEqual(ALPHABETIC, get_advanced_structural_type(self.data["constant_str"]))
        self.assertEqual(ALPHABETIC,
                         get_advanced_structural_type(self.data["id_text_column"]))
        self.assertEqual(ALL,
                         get_advanced_structural_type(self.str_data["word_all"]))
        self.assertEqual(ALPHANUMERIC,
                         get_advanced_structural_type(self.data["id_column_both"]))
        self.assertEqual(MULTIPLE_VALUES,
                         get_advanced_structural_type(self.str_data["multiple"]))
        self.assertEqual(PHRASE,
                         get_advanced_structural_type(self.str_data["phrase"]))
        self.assertEqual(SENTENCE,
                         get_advanced_structural_type(self.str_data["sentence"]))
        self.assertEqual(ARTICLE,
                         get_advanced_structural_type(self.str_data["article"]))

        self.assertEqual(DATE, get_advanced_structural_type(self.str_data["MM.DD.YYYY"]))
        self.assertEqual(DATE, get_advanced_structural_type(self.str_data["DDMonYYYY"]))


class TestDateTime(unittest.TestCase):
    def setUp(self):
        self.data = {
            'MM-DD-YYYY': ['11-04-1999', '12-31-1999', '01-03-1999'],
            'M-D-YY': ['11-4-99', '12-31-99', '1-3-99'],
            'MM.DD.YYYY': ['11.4.1999', '12.31.1999', '1.3.1999'],
            'MM.DD.YYYY_': ['11. 4. 1999', '12. 31. 1999', '1. 3. 1999'],
            'MM.DD.YY': ['11.04.99', '12.31.99', '01.03.99'],
            'MM/DD/YY': ['11/04/99', '12/31/99', '01/03/99', '2/4/95'],
            'DD/MM/YY': ['11/04/99', '31/12/99', '03/01/99', '4/2/95'],
            'MM/DD/YYYY': ['11/4/1999', '12/31/1999', '1/3/1999'],
            'YYYY,DDMon': ['1999,4Feb', '1999,31Jan', '1999,3Nov'],
            'YYYY,DDMonth': ['1999,4February', '1999,31January', '1999,3November'],
            'YYYY,DD Mon': ['1999,4 Feb', '1999,31 Jan', '1999,3 Nov'],
            'YYYY,DD Month': ['1999,4 February', '1999,31 January', '1999,3 November'],
            'MonDD,YYYY': ['Feb4,1999', 'Jan 31,1999', 'Nov 3, 1999'],
            'MonthDD,YYYY': ['February4,1999', 'January 31,1999', 'November 3, 1999'],
            'DDMonth,YYYY': ['4February,1999', '31 January,1999', '3 November, 1999 '],
            'DDMon,YYYY': ['4Feb,1999', '31 Jan,1999', '3 Nov, 1999 '],
            'DDMonthYYYY': ['4February1999', '31January 1999', '3 November 1999 '],
            'DDMonYYYY': ['4Feb1999', '31Jan 1999', '3 Nov 1999 '],
            'YY/MM/DD': ['95/2/4', '99/12/31', '05/2/3', '00/2/3'],
            'DD-Mon-YYYY': ['04-Feb-1995', '03-APR-1999', '31-JUL-1999'],
            'DD-Month-YYYY': ['4-February-1995', '03-April-1999', '31-July-1999'],

            # ISO 8601 https://www.cl.cam.ac.uk/~mgk25/iso-time.html
            'YYYY-MM-DD': ['1995-02-04', '2000-12-31', '1999-01-03', '2024-07-29', '1997-10-01', '2024-11-30'],
            'YYYY-MM': ['1995-02', '2000-12', '1999-01', '2024-07', '1997-10', '2024-11'],
            'YYYYMMDD': ['19950204', '20001231', '19990103', '20240729', '19971001', '20241130'],
          
            'Week': ['1997-W01', '1997W01', '1995W05', '2023-W03', '2024-W50'],  # 1997-W01 or 1997W01 (first week of the year 1997)
            'Week_day': ['1997-W01-3', '1997W013', '1995W0512', '2023-W03-2', '2024-W50-1'],  # 1997-W01-3 or 1997W013 (#rd day of the first week of the year 1997) 1995-W05-12 or 1995W0512 (12th day of the fifth week of the year 1995)
            'Days': ['1995-035', '1995035', '2024340'],  # 1995-035 or 1995035 (35th day of the year 1995)
            'Year': ['1995', '2000', '2024'],

            # time and timezones
            'Time_:': ['12:34', '23:59:59', '00:00:00', 'T12:34:12.123', 'T12:34:12', 'T03:24'],
            'Time': ['T123412.123', 'T123412', 'T0324'],
            'Time:zone': ['12:34:56Z', 'T144515Z', 'T12:30+02:00', 'T12:30−02:00', 'T12:30+02', 'T12:30-0200'],

            'Time_and_date': ['1995-02-04T12:34', '2000-12-31T23:59:59', '1999-01-03T00:00:00',
                              '2024-07-29T12:34:12.123', '1997-10-01T123412', '2024-11-30T0324'],
            'Time_zone': ['1995-02-04T12:34:56Z', '2000-12-31T14:30Z', '1999-01-03T00:00:00Z',
                          '2007-04-05T12:30−02:00'],
            # EPOCH time - number of seconds from 1970-01-01T00:00:00Z
            'epoch': ['649213200', '1722241808']  # 649213200 (1990/7/29) 1722241808 (2024/7/29)
        }
        self.not_dates = {
            'first': ['1999,4Monuary'],
            'second': ['1999,4 Mon'],
            'third': ['1995-02-0400'],
            'fourth': ['1995-0350'],
            'fifth': ['17222418000'],
            'sixth': ['1722A41808']
        }

    def test_date(self):
        for i in self.data:
            print(f"{i} : {self.data[i]}\n")
            self.assertTrue(is_date(pd.Series(self.data[i])))
        for i in self.not_dates:
            self.assertFalse(is_date(pd.Series(i)))


class TestTypesComparing(unittest.TestCase):
    def test_basic_types(self):

        self.assertNotEqual(NONNUMERICAL, DATE)
        self.assertNotEqual(NONNUMERICAL, NUMERICAL)
        self.assertNotEqual(NUMERICAL, DATE)

        self.assertEqual(NUMERICAL, NUMERICAL)
        self.assertEqual(DATE, DATE)
        self.assertEqual(NONNUMERICAL, NONNUMERICAL)

    def test_advanced_types(self):
        self.assertTrue(issubclass(INT, NUMERICAL))
        self.assertTrue(issubclass(FLOAT, NUMERICAL))
        self.assertTrue(issubclass(NUMERICAL, NUMERICAL))
        self.assertTrue(issubclass(NONNUMERICAL, NONNUMERICAL))
        self.assertTrue(issubclass(NONNUMERICAL, NONNUMERICAL))
        self.assertTrue(issubclass(UNDEFINED, UNDEFINED))
        self.assertTrue(issubclass(DATE, DATE))

    def test_structural_types(self):
        self.assertTrue(issubclass(HUMAN_GENERATED, NUMERICAL))
        self.assertTrue(issubclass(COMPUTER_GENERATED, NUMERICAL))
        self.assertFalse(issubclass(HUMAN_GENERATED, NONNUMERICAL))
        self.assertFalse(issubclass(COMPUTER_GENERATED, NONNUMERICAL))

        self.assertTrue(issubclass(MULTIPLE_VALUES, NONNUMERICAL))
        self.assertTrue(issubclass(WORD, NONNUMERICAL))
        self.assertTrue(issubclass(PHRASE, NONNUMERICAL))
        self.assertTrue(issubclass(ARTICLE, NONNUMERICAL))
        self.assertTrue(issubclass(SENTENCE, NONNUMERICAL))

        self.assertTrue(issubclass(ALPHABETIC, NONNUMERICAL))
        self.assertTrue(issubclass(ALL, NONNUMERICAL))
        self.assertTrue(issubclass(ALPHANUMERIC, NONNUMERICAL))


if __name__ == '__main__':
    unittest.main()
