import dataclasses
import enum
import re
from enum import Enum, EnumMeta, StrEnum
from typing import Any
from dateutil.parser import parse, ParserError

import numpy as np
import pandas as pd


class TypeSettings:
    categorical_big_threshold = 0.9
    categorical_small_threshold = 0.7
    categorical_small_dataset = 50


class SuperNestedEnum(Enum):
    # reference: https://stackoverflow.com/questions/54488648/how-to-make-nested-enum-also-have-value
    def __new__(cls, *args):
        obj = object.__new__(cls)
        value = None
        # Normal Enumerator definition
        if len(args) == 1:
            value = args[0]

        # Have a tuple of values, first de value and next the nested enum (I will set in __init__ method)
        if len(args) == 2:
            value = args[0]

        if value:
            obj._value_ = value

        return obj

    def __init__(self, name, nested=None):
        # At this point you can set any attribute what you want
        if nested:
            # Check if is an Enumerator you can comment this if. if you want another object
            if isinstance(nested, EnumMeta):
                for enm in nested:
                    self.__setattr__(enm.name, enm)


def is_id(column: pd.Series) -> bool:
    """
    The column is id if all values
    are uniq and values are numerical or length
     of string is smaller than threshold
    :param column: to check
    :return: true if the column is id
    """
    max_id_length = 6
    # length of values is smaller than 6?
    return (column.nunique() == column.size
            )  # and (is_numerical(column) or column.str.len().max() <= max_id_length))


def is_bool(column: pd.Series) -> bool:
    """
    If the column contains only two values it could be transferred into bool
    :param column: to check
    :return: true for bool column
    """
    try:
        lower = column.map(str.lower)
        return lower.nunique() == 2
    except:
        return column.nunique() == 2


def is_constant(column: pd.Series) -> bool:
    """
    If the column contains only one value
    :param column: to check
    :return: true if the values are constant
    """
    return column.nunique() == 1


# def is_bool(column: pd.Series) -> bool:
#     """
#     Decide if type is bool
#     :param column:
#     :return: True if type is boolean
#     """
#     if np.issubdtype(column.dtype, np.bool_):
#         return True
#     return type(column.mode()[0]) is bool


def is_numerical(x: pd.Series) -> bool:
    """
    Decide if np type is numerical
    :param x: the type
    :return: true if it is numerical, otherwise false
    """
    try:
        to_numeric = x.apply(lambda s: pd.to_numeric(s.replace(',', '.'), errors='coerce'))
    except AttributeError:
        to_numeric = x.apply(lambda s: pd.to_numeric(s, errors='coerce'))
    return to_numeric.any() and to_numeric.dtype != bool


def is_int(x: pd.Series) -> bool:
    """
    Decide if numerical type is integer
    :param x: the series for decide
    :return: true if it is integer, otherwise false
    """
    to_numeric = x.apply(lambda s: pd.to_numeric(s, errors='coerce'))  ## todo time efficiency we could do that before
    return np.issubdtype(to_numeric, np.integer) or to_numeric.apply(float.is_integer).all()


def is_human_gen(x: pd.Series) -> bool:
    """
     Decide if float number is human generated
     :param x: the series for decide
     :return: true if it is human generated, otherwise false
     """

    def floating_length_gt(num: Any, gt: int):
        """
        Returns true if count of number after floating point is grater then gt
        :param num: to decide
        :param gt: threshold
        """
        splitted = str(num).split(".")
        if len(splitted) > 1:
            return len(splitted[1]) > gt
        return False

    try:
        to_numeric = x.apply(lambda s: pd.to_numeric(s.replace(',', '.'), errors='coerce'))
    except AttributeError:
        to_numeric = x.apply(lambda s: pd.to_numeric(s, errors='coerce'))
    ## todo time efficiency
    return to_numeric.apply(lambda s: not floating_length_gt(s, 3)).all()


def is_not_numerical(x: pd.Series) -> bool:
    return x.map(type).eq(str).all() and not is_numerical(x)


def is_categorical(x: pd.Series) -> bool:
    numer_uniq = x.nunique()
    size = x.size
    diff = size - numer_uniq
    perc_diff = diff / size
    if size > TypeSettings.categorical_small_dataset and perc_diff >= TypeSettings.categorical_big_threshold:
        return True
    return size <= TypeSettings.categorical_small_dataset and perc_diff >= TypeSettings.categorical_small_threshold


def is_word(x: pd.Series) -> bool:
    def is_str_word(word: str):
        return word.count(" ") == 0

    return x.apply(lambda s: is_str_word(s)).all()


def is_phrase(x: pd.Series) -> bool:
    def is_str_phrase(word: str):
        return word.count(".") == 0

    return x.apply(lambda s: is_str_phrase(s)).all() and not is_word(x)


def is_sentence(x: pd.Series) -> bool:
    def is_str_sentence(word: str):
        return ((word.endswith(".") or word.endswith("!") or word.endswith("?")) and word.count(".") <= 1
                and word.count("!") <= 1 and word.count("?") <= 1) and re.search("^[A-Z]", word)

    return x.apply(lambda s: is_str_sentence(s)).all()

def is_article(x: pd.Series) -> bool:
    return not is_word(x) and not is_phrase(x) and not is_sentence(x) and not is_multiple(x)

def is_multiple(x: pd.Series) -> bool:
    def is_str_multiple(word: str):
        regex = re.compile('[a-zA-Z0-9]')
        word_clean = regex.sub('', word)
        res = "".join(dict.fromkeys(word_clean))
        return (word.count(res) == word_clean.count(res) and word_clean.count(res) > 0) or res == ''

    return x.apply(lambda s: is_str_multiple(s)).all()

def is_date(column: pd.Series) -> bool:
    """
    Decide if type of column is date
    :param column:
    :return:
    """

    def is_str_date(word: str):
        try:
            parse(word, fuzzy_with_tokens=True)
            return True
        except ParserError:
            element = str(word).strip()
            one_or_two = '(\d{1}|\d{2})'
            two_or_four = '(\d{2}|\d{4})'
            months = '(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|June|July|Aug|Sept|Oct|Nov|Dec)'
            pattern = r'|' + r'^(\d{1}|\d{2}|{\d{4}}),(\d{1}|\d{2}) ' + months  # + '$'  # 1999,4 Feb 1999,4 February
            pattern = pattern + '|' + r'^' + one_or_two + '\. ' + one_or_two + '\. ' + two_or_four  #11. 4. 1999
            pattern = pattern + '|' + r'^(\d{1}|\d{2}|{\d{4}}),(\d{1}|\d{2})' + months  #1999,4February 1999,4Feb
            if re.match(pattern, element):
                return True
            else:
                return False

    return column.apply(lambda s: is_str_date(s)).all()

    element = str(column.mode()[0]).strip()
    one_or_two = '(\d{1}|\d{2})'
    two_or_four = '(\d{2}|\d{4})'
    months = '(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|June|July|Aug|Sept|Oct|Nov|Dec)'
    pattern = r'^' + one_or_two + '-' + one_or_two + '-' + two_or_four  # + '$'  # 11-03-1999 / 11-3-99
    pattern = pattern + '|' + r'^' + one_or_two + '\.' + one_or_two + '\.' + two_or_four  # + '$' # 11.3.1999 / 11.03.99
    pattern = pattern + '|' + r'^' + one_or_two + '/' + one_or_two + '/' + two_or_four  # + '$' # 11/3/1999 11/03/99
    pattern = pattern + '|' + r'^(\d{1}|\d{2}|{\d{4}}),(\d{1}|\d{2})' + months  # + '$'  # 2022,17Feb / 2022,17February
    pattern = pattern + '|' + r'^' + months + '(\d{1}|\d{2}),(\d{4}|\d{2})$'  # Feb17,2022 / February17,2022
    pattern = pattern + '|' + r'^(\d{1}|\d{2})' + months + ',(\d{4}|\d{2})$'  # 17February,2022 /  17Feb,2022
    if re.match(pattern, element):
        return True
    else:
        return False


def is_string(column: pd.Series) -> bool:
    """
    :param column:
    :return: True if column type is string, False otherwise
    """
    common = column.value_counts().nlargest(10)
    for i in common.keys():
        if type(i) != str or (" " in i and len(i) > 100):
            return False
    return True


def is_text(column: pd.Series) -> bool:
    """
    :param column:
    :return: True if column type is text, False otherwise
    """
    common = column.value_counts().nlargest(10)
    for i in common.keys():
        if type(i) != str or (" " in i and len(i) < 100):
            return False
    return True


def get_data_kind(column: pd.Series) -> "DataKind":
    """
    Indicates kind of column.

    :param column: to indicate
    :return: detected kind
    """
    if is_bool(column):
        return DataKind.BOOL
    if is_id(column):
        return DataKind.ID
    if is_constant(column):
        return DataKind.CONSTANT
    else:
        return DataKind.UNDEFINED


class DataKind(Enum):
    BOOL = "bool"
    ID = "id"
    CONSTANT = "constant"
    UNDEFINED = "undefined"


## todo make better more accurate
## TODO switch
def get_type(column: pd.Series) -> Any:
    """
    Indicates type of column.

    :param column: to indicate
    :return: detected type
    """
    if is_numerical(column.dtype):
        return Types.NUMERICAL
    if np.issubdtype(column.dtype, np.integer):
        return Types.NUMERICAL.value.INT
    if np.issubdtype(column.dtype, np.floating):
        return Types.NUMERICAL.value.FLOAT
    if is_bool(column):
        return Types.BOOL  # todo test this
    if is_date(column):
        return Types.NONNUMERICAL.value.TEXT.value.DATE
    if is_string(column):
        return Types.NONNUMERICAL.value.TEXT.value.WORD
    if is_text(column):
        return Types.NONNUMERICAL.value.TEXT.value.ARTICLE
    else:
        return Types.UNDEFINED


class _Float(Enum):
    HUMAN_GENERATED = "human_generated"
    COMPUTER_GENERATED = "computer_generated"


class _Numerical(Enum):
    FLOAT = _Float
    INT = "int"
    DATE = "date"


class _Categorical(Enum):
    ORDINAL = "ordinal"
    NOMINAL = "nominal"


class _Word(Enum):
    NUMERIC = "numeric"
    ALPHABETIC = "alphabetic"
    ALPHANUMERIC = "alphanumeric"
    ALL = "all"


class _Text(Enum):
    WORD = "word", _Word
    SENTENCE = "sentence"
    PHRASE = "phrase"  # max 4 words without punctuation
    ARTICLE = "article"
    DATE = "date"
    MULTIPLE_VALUES = "multiple"  # genres name : "Action, Adventure, Drama"


class _NonNumerical(Enum):
    CATEGORICAL = _Categorical
    TEXT = _Text


class Types(Enum):
    """
    Enum class representing column type
    """
    NUMERICAL = _Numerical
    # INT = 5
    # FLOAT = 6

    NONNUMERICAL = _NonNumerical
    # DATE = 7
    # STRING = 3
    # TEXT = 4
    UNDEFINED = "undefined"
