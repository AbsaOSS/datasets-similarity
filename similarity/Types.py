import re
from enum import Enum
from typing import Any
from dateutil.parser import parse, ParserError

import numpy as np
import pandas as pd


class TypeSettings:
    categorical_big_threshold = 0.9
    categorical_small_threshold = 0.7
    categorical_small_dataset = 50


def is_id(column: pd.Series) -> bool:
    """
    The column is id if all values
    are uniq
    :param column: to check
    :return: true if the column is id
    """
    return column.nunique() == column.size


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
    return to_numeric.any() and (to_numeric.dtype == np.float64 or to_numeric.dtype == np.int64) and not to_numeric.isnull().values.all()


def is_int(x: pd.Series) -> bool:
    """
    Decide if numerical type is integer
    :param x: the series for decide
    :return: true if it is integer, otherwise false
    """
    try:
        to_numeric = x.apply(lambda s: pd.to_numeric(s.replace(',', '.'), errors='coerce'))
    except AttributeError:
        to_numeric = x.apply(lambda s: pd.to_numeric(s, errors='coerce'))  ## todo time efficiency we could do that before
    return np.issubdtype(to_numeric, np.integer) or to_numeric.dropna().apply(float.is_integer).all()


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
    """
     Decide if  type is not numerical
     :param x: the series for decide
     :return: false if it is numerical, otherwise true
     """
    return x.apply(lambda s: str(s)).all() and not is_numerical(x)


def is_categorical(x: pd.Series) -> bool:
    """
    Categorical def from : https://jeffreymorgan.io/articles/identifying-categorical-data/#:~:text=Calculate%20the%20difference%20between%20the,is%20composed%20of%20categorical%20values

    :param x: the series for decide
    :return: true for categorical
    """
    numer_uniq = x.nunique()
    size = x.size
    diff = size - numer_uniq
    perc_diff = diff / size
    if size > TypeSettings.categorical_small_dataset and perc_diff >= TypeSettings.categorical_big_threshold:
        return True
    return size <= TypeSettings.categorical_small_dataset and perc_diff >= TypeSettings.categorical_small_threshold


def is_word(x: pd.Series) -> bool:
    """
    the string is word if it does not have any spaces

    :param x: series for decide
    :return: true for word
    """

    def is_str_word(word: str):
        return word.strip().count(" ") == 0

    return x.apply(lambda s: is_str_word(s)).all()


def is_word_by_regex(x: pd.Series, pattern: str) -> bool:
    """

    :param x: series for decide
    :return: true if all words matches regex
    """

    def is_by_regex(word: str):
        if re.match(pattern, word):
            return True
        return False

    return x.apply(lambda s: is_by_regex(s)).all()


def is_alphabetic_word(x: pd.Series) -> bool:
    """
    the word is alphabetic if contains only A-Z and a-z

    :param x: series for decide
    :return: true for alphabetic
    """
    pattern = "^[A-Za-z]*$"
    return is_word_by_regex(x, pattern)


def is_alphanumeric_word(x: pd.Series) -> bool:
    """
    the word is alphanumeric if contains only A-Z and a-z

    :param x: series for decide
    :return: true for alphanumeric
    """
    pattern = "^[A-Za-z0-9]*$"
    return is_word_by_regex(x, pattern)


def is_phrase(x: pd.Series) -> bool:
    """
    The string is phrase if it does not contain any dots

    :param x:  series for decide
    :return:  true for phrase
    """

    def is_str_phrase(word: str):
        return word.count(".") == 0

    return x.apply(lambda s: is_str_phrase(s)).all() and not is_word(x)


def is_sentence(x: pd.Series) -> bool:
    """
    The string is sentence if it starts with uperCasse letter and end with interpunction

    :param x:  series for decide
    :return:  true for sentence
    """

    def is_str_sentence(word: str):
        return ((word.endswith(".") or word.endswith("!") or word.endswith("?")) and word.count(".") <= 1
                and word.count("!") <= 1 and word.count("?") <= 1) and re.search("^[A-Z]", word)

    return x.apply(lambda s: is_str_sentence(s)).all()


def is_article(x: pd.Series) -> bool:
    """
    The string is article if it not word, phrase, sentence or multiple

    :param x:  series for decide
    :return:  true for article
    """
    return not is_word(x) and not is_phrase(x) and not is_sentence(x) and not is_multiple(x)


def is_multiple(x: pd.Series) -> bool:
    """
    The string is multiple if the record is split by some sequence

    :param x:  series for decide
    :return:  true for multiple
    """

    def is_str_multiple(word: str):
        regex = re.compile('[a-zA-Z0-9]')
        word_clean = regex.sub('', word)
        res = "".join(dict.fromkeys(word_clean))
        return (word.count(res) == word_clean.count(res) and word_clean.count(res) > 0) or res == '' and res != ' '

    return x.apply(lambda s: is_str_multiple(s)).all()


def is_true_multiple(x: pd.Series) -> bool:
    """
    The string is true multiple if the record is split by some sequence and the sequence is the same for all rows

    :param x:  series for decide
    :return:  true for multiple
    """

    def is_str_multiple(word: str):
        regex = re.compile('[a-zA-Z0-9]')
        word_clean = regex.sub('', word)
        res = "".join(dict.fromkeys(word_clean))
        return res

    result_arr = x.apply(lambda s: is_str_multiple(s)).values
    to_return = [i for i in result_arr if (i != '')]
    if len(to_return) == 0:
        return True
    if to_return[0].replace(" ", "") == '':
        return False
    return to_return.count(to_return[0]) == len(to_return)


def is_date(column: pd.Series) -> bool:
    """
    Decide if type of column is date
    We are using date parser

    :param column: series for decide
    :return:true for date
    """

    def is_str_date(word: str):
        try:
            parse(str(word), fuzzy_with_tokens=True)  # todo add timezone
            return True
        except ParserError:
            element = str(word).strip()
            one_or_two = '(\d{1}|\d{2})'
            two_or_four = '(\d{2}|\d{4})'
            months = '(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|June|July|Aug|Sept|Oct|Nov|Dec)'
            pattern = r'^(\d{1}|\d{2}|\d{4}),(\d{1}|\d{2}) ' + months  # + '$'  # 1999,4 Feb 1999,4 February
            pattern = pattern + '|' + r'^' + one_or_two + '\. ' + one_or_two + '\. ' + two_or_four  # 11. 4. 1999
            pattern = pattern + '|' + r'^(\d{1}|\d{2}|\d{4}),(\d{1}|\d{2})' + months  # 1999,4February 1999,4Feb
            if re.match(pattern, element):
                return True
            else:
                return False

    return column.apply(lambda s: is_str_date(s)).all()


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


def get_basic_type(column: pd.Series) -> Any:
    """
    Indicates type of column but only numerical, date, not numerical

    :param column: to indicate
    :return: detected type
    """
    if is_numerical(column):
        return Types.NUMERICAL
    if is_date(column):  # todo what about year?
        return Types.DATE
    if is_not_numerical(column):
        return Types.NONNUMERICAL
    else:
        return Types.UNDEFINED


def get_advanced_type(column: pd.Series) -> Any:
    """
    Indicates type of column int, float, date, text, categorical

    :param column: to indicate
    :return: detected type
    """
    if is_numerical(column):
        if is_int(column):
            return Types.NUMERICAL.value.INT
        else:
            return Types.NUMERICAL.value.FLOAT
    if is_date(column):  # todo what about year?
        return Types.DATE
    if is_not_numerical(column):
        if is_categorical(column):
            return Types.NONNUMERICAL.value.CATEGORICAL
        else:
            return Types.NONNUMERICAL.value.TEXT
    else:
        return Types.UNDEFINED


def get_advanced_structural_type(column: pd.Series) -> Any:
    """
    Indicates type of column int, float - human, computer, date, text - word, sentence, phrase article, multiple, categorical

    :param column: to indicate
    :return: detected type
    """
    if is_numerical(column):
        if is_int(column):
            return Types.NUMERICAL.value.INT
        else:
            if is_human_gen(column):
                return Types.NUMERICAL.value.FLOAT.value.HUMAN_GENERATED
            return Types.NUMERICAL.value.FLOAT.value.COMPUTER_GENERATED
    if is_date(column):
        return Types.DATE
    if is_not_numerical(column):
        column = column.apply(lambda s: str(s))
        if is_categorical(column):
            return Types.NONNUMERICAL.value.CATEGORICAL
        else:
            if is_word(column):
                if is_alphabetic_word(column):
                    return Types.NONNUMERICAL.value.TEXT.value.WORD.value.ALPHABETIC
                if is_alphanumeric_word(column):
                    return Types.NONNUMERICAL.value.TEXT.value.WORD.value.ALPHANUMERIC
                return Types.NONNUMERICAL.value.TEXT.value.WORD.value.ALL
            if is_true_multiple(column):
                return Types.NONNUMERICAL.value.TEXT.value.MULTIPLE_VALUES
            if is_sentence(column):
                return Types.NONNUMERICAL.value.TEXT.value.SENTENCE
            if is_phrase(column):
                return Types.NONNUMERICAL.value.TEXT.value.PHRASE
            if is_article(column):
                return Types.NONNUMERICAL.value.TEXT.value.ARTICLE
            return Types.NONNUMERICAL.value.TEXT
    else:
        return Types.UNDEFINED


class _Float(Enum):
    HUMAN_GENERATED = "human_generated"
    COMPUTER_GENERATED = "computer_generated"


class _Numerical(Enum):
    FLOAT = _Float
    INT = "int"


class _Categorical(Enum):
    ORDINAL = "ordinal"
    NOMINAL = "nominal"


class _Word(Enum):
    ALPHABETIC = "alphabetic"
    ALPHANUMERIC = "alphanumeric"
    ALL = "all"


class _Text(Enum):
    WORD = _Word
    SENTENCE = "sentence"
    PHRASE = "phrase"  # max 4 words without punctuation
    ARTICLE = "article"
    MULTIPLE_VALUES = "multiple"  # genres name : "Action, Adventure, Drama"


class _NonNumerical(Enum):
    CATEGORICAL = _Categorical
    TEXT = _Text


class Types(Enum):
    """
    Enum class representing column type
    """
    NUMERICAL = _Numerical
    NONNUMERICAL = _NonNumerical
    DATE = "date"
    UNDEFINED = "undefined"
