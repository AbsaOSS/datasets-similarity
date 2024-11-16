"""
This files contains all
"""

import re
from enum import Enum
from typing import Any
from dateutil.parser import parse, ParserError

import numpy as np
import pandas as pd


class TypeSettings:
    """
    This class represents settings for deciding data types.

    categorical_big_threshold is threshold for large datasets
    categorical_small_threshold is threshold for small datasets
    small dataset has size smaller than categorical_small_dataset
    large dataset has size bigger than categorical_small_dataset

    threshold is comparison for size of dataset minus number of uniq values divided by size
    threshold = (size_dataset - uniq_count) / size_dataset

    computer_generated_threshold is threshold for number of numbers after decimal point

    """

    categorical_big_threshold = 0.9
    categorical_small_threshold = 0.7
    categorical_small_dataset = 50

    computer_generated_threshold = 3


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
    except TypeError:
        return column.nunique() == 2


def is_constant(column: pd.Series) -> bool:
    """
    If the column contains only one value, the column is constant

    :param column: to check
    :return: true if the values are constant
    """
    return column.nunique() == 1


def series_to_numeric(x: pd.Series) -> pd.Series:
    """
    Apply to_numeric on pd.Series
    :param x:
    :return: numeric series
    """
    try:
        to_numeric = x.apply(
            lambda s: pd.to_numeric(
                s.replace(",", "."),
                errors="coerce",
            )
        )
    except AttributeError:
        to_numeric = x.apply(lambda s: pd.to_numeric(s, errors="coerce"))
    return to_numeric


def is_numerical(x: pd.Series) -> bool:
    """
    Decide if column type is numerical.

    Column is numerical if it could be transferred into numeric,
    and it is float or int, and it is not full nulls

    :param x: the type
    :return: true if it is numerical, otherwise false
    """
    return x.any() and (x.dtype in (np.float64, np.int64)) and not (x.isnull().values.sum() / x.size > 0.9)


def is_int(x: pd.Series) -> bool:
    """
    Decide if numerical type is integer

    Column is int if is subtype of integer or is float, but it could be transferred into integer.

    :param x: the series for decide
    :return: true if it is integer, otherwise false
    """
    return np.issubdtype(x, np.integer) or x.dropna().apply(float.is_integer).all()


def is_human_gen(x: pd.Series) -> bool:
    """
    Decide if float number is human generated

    Float is human generated if number of numbers after decimal
    point is smaller than computer_generated_threshold

    :param x: the series for decide
    :return: true if it is human generated, otherwise false
    """

    def floating_length_gt(num: Any, gt: int) -> bool:
        """
        Returns true if count of number after floating point is grater then gt
        :param num: to decide
        :param gt: threshold
        """
        split = str(num).split(".")
        if len(split) > 1:
            return len(split[1]) > gt
        return False

    return x.apply(
        lambda s: not floating_length_gt(
            s,
            TypeSettings.computer_generated_threshold,
        )
    ).all()


def is_not_numerical(x: pd.Series) -> bool:
    """
    Decide if  type is not numerical
    The column is not numerical if it is not numerical, and it could be transferred to string

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
    The string is word if it does not have any spaces

    :param x: series for decide
    :return: true for word
    """

    def is_str_word(word: str) -> bool:
        return word.strip().count(" ") == 0

    return x.apply(lambda s: is_str_word(s)).all()


def is_word_by_regex(x: pd.Series, pattern: str) -> bool:
    """
    Decide if the word is same as regex

    :param pattern: for regex
    :param x: series for decide
    :return: true if all words matches regex
    """

    def is_by_regex(word: str) -> bool:
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

    def is_str_phrase(word: str) -> bool:
        return word.count(".") == 0

    return x.apply(lambda s: is_str_phrase(s)).all() and not is_word(x)


def is_sentence(x: pd.Series) -> bool:
    """
    The string is sentence if it starts with upperCase letter and end with fullstops.

    :param x:  series for decide
    :return:  true for sentence
    """

    def is_str_sentence(word: str) -> bool:
        return (
            (word.endswith(".") or word.endswith("!") or word.endswith("?")) and word.count(".") <= 1 and word.count("!") <= 1 and word.count("?") <= 1
        ) and re.search("^[A-Z]", word)

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

    def is_str_multiple(word: str) -> bool:
        regex = re.compile("[a-zA-Z0-9]")
        word_clean = regex.sub("", word)
        res = "".join(dict.fromkeys(word_clean))
        return (word.count(res) == word_clean.count(res) and word_clean.count(res) > 0) or res == "" and res != " "

    return x.apply(lambda s: is_str_multiple(s)).all()


def is_true_multiple(x: pd.Series) -> bool:
    """
    The string is true multiple if the record is split
    by some sequence and the sequence is the same for all rows

    :param x:  series for decide
    :return:  true for multiple
    """

    def is_str_multiple(word: str) -> str:
        regex = re.compile("[a-zA-Z0-9]")
        word_clean = regex.sub("", word)
        res = "".join(dict.fromkeys(word_clean))
        return res

    result_arr = x.apply(lambda s: is_str_multiple(s)).values
    to_return = [i for i in result_arr if i != ""]
    if len(to_return) == 0:
        return True
    if to_return[0].replace(" ", "") == "":
        return False
    return to_return.count(to_return[0]) == len(to_return)


def is_date(column: pd.Series) -> bool:
    """
    Decide if type of column is date
    We are using date parser

    :param column: series for decide
    :return:true for date
    """

    def is_str_date(word: str) -> bool:
        element = str(word).strip()
        try:
            parse(element, fuzzy=True)
            return True
        except (ParserError, OverflowError):
            one_or_two = r"(\d{1}|\d{2})"
            two_or_four = r"(\d{2}|\d{4})"
            months = (
                "(January|February|March|April|May|June|July|August|"
                "September|October|November|December|Jan|Feb"
                "|Mar|Apr|May|June|July|Aug|Sept|Oct|Nov|Dec)"
            )
            date_pattern = r"^(T(\d{6}|\d{4})(|.\d{3})(|Z))$"
            pattern = date_pattern
            # + '$'  # 1999,4 Feb 1999,4 February
            pattern = pattern + "|" + r"^(\d{1}|\d{2}|\d{4}),(\d{1}|\d{2}) " + months
            # 11. 4. 1999
            pattern = pattern + "|" + r"^" + one_or_two + r"\. " + one_or_two + r"\. " + two_or_four
            # 1999,4February 1999,4Feb
            pattern = pattern + "|" + r"^(\d{1}|\d{2}|\d{4})," + one_or_two + months
            # '99/12/31', '05/2/3' 00/2/3
            pattern = pattern + "|" + r"^" + two_or_four + r"/" + one_or_two + r"/" + one_or_two
            # 1995W05 2024-W50
            pattern = pattern + "|" + r"^(\d{4}(W|-W)\d{2})"
            # 1995W0512  2023-W03-2
            pattern = pattern + "|" + r"(\d{4}(W|-W)\d{2}(-|)" + one_or_two + ")$"
            # '1995-035', '1995035', '2024340'
            pattern = pattern + "|" + r"^((2|1)\d{3}-\d{3})$|(^(2|1)\d{6})$"
            # epoch time 1911517200(2030 will be max for us)
            pattern = pattern + "|" + r"(^\d{1,10})$"

            return bool(re.match(pattern, element))

    return column.apply(lambda s: is_str_date(s)).all()


def get_data_kind(
    column: pd.Series,
) -> "DataKind":
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
    if is_categorical(column):
        return DataKind.CATEGORICAL
    return DataKind.UNDEFINED


class DataKind(Enum):
    """
    Represents all data kind.
    """

    BOOL = "bool"
    ID = "id"
    CONSTANT = "constant"
    UNDEFINED = "undefined"
    CATEGORICAL = "categorical"


def get_basic_type(column: pd.Series) -> Any:
    """
    Indicates type of column but only numerical, date, not numerical

    :param column: to indicate
    :return: detected type
    """
    if is_numerical(series_to_numeric(column)):
        return NUMERICAL
    if is_date(column):  # todo what about year?
        return DATE
    if is_not_numerical(column):
        return NONNUMERICAL
    return UNDEFINED


def get_advanced_type(column: pd.Series) -> Any:
    """
    Indicates type of column int, float, date, text

    :param column: to indicate
    :return: detected type
    """
    column_num = series_to_numeric(column)
    if is_numerical(column_num):
        if is_int(column_num):
            return INT
        return FLOAT
    if is_date(column):  # todo what about year?
        return DATE
    if is_not_numerical(column):
        return NONNUMERICAL
    return UNDEFINED


def get_advanced_structural_type(
    column: pd.Series,
) -> Any:
    """
    Indicates type of column int, float - human, computer, date,
    text - word, sentence, phrase article, multiple

    :param column: to indicate
    :return: detected type
    """
    column_num = series_to_numeric(column)
    if is_numerical(column_num):
        if is_int(column_num):
            return INT
        if is_human_gen(column_num):
            return HUMAN_GENERATED
        return COMPUTER_GENERATED
    if is_date(column):
        return DATE
    if is_not_numerical(column):
        column = column.apply(lambda s: str(s))
        if is_word(column):
            if is_alphabetic_word(column):
                return ALPHABETIC
            if is_alphanumeric_word(column):
                return ALPHANUMERIC
            return ALL
        if is_true_multiple(column):
            return MULTIPLE_VALUES
        if is_sentence(column):
            return SENTENCE
        if is_phrase(column):
            return PHRASE
        if is_article(column):
            return ARTICLE
        return NONNUMERICAL
    return UNDEFINED


class Type:
    """
    Base class for type
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return ""


class DATE(Type):
    """
    Represents type date.
    """

    def __str__(self):
        return "DATE"


class UNDEFINED(Type):
    """
    Represents class undefined
    """

    def __str__(self):
        return "UNDEFINED"


class NUMERICAL(Type):
    """
    Represents numerical types.
    """

    def __str__(self):
        return "NUMERICAL"


class INT(NUMERICAL):
    """
    Represents INT type.
    """

    def __str__(self):
        return "INT"


class FLOAT(NUMERICAL):
    """
    Represents FLOAT type.
    """

    def __str__(self):
        return "FLOAT"


class HUMAN_GENERATED(FLOAT):
    """
    Represents float, which is probably generated by human.
    Number of numbers after floating point is small or rounded.
    """

    def __str__(self):
        return "HUMAN_GENERATED"


class COMPUTER_GENERATED(FLOAT):
    """
    Represents float, which is probably generated by computer.
    Number of numbers after floating point is bigger or not rounded.
    """

    def __str__(self):
        return "COMPUTER_GENERATED"


class NONNUMERICAL(Type):
    """
    Subclass for nonnumerical types
    """

    def __str__(self):
        return "NONNUMERICAL"


class WORD(NONNUMERICAL):
    """
    Word is string without spaces.
    """

    def __str__(self):
        return "WORD"


class ALPHABETIC(WORD):
    """
    This type is WORD, it contains only letters (a-z)
    """

    def __str__(self):
        return "ALPHABETIC"


class ALPHANUMERIC(WORD):
    """
    This type is WORD, it contains only letters (a-z) and numbers (0-9)
    """

    def __str__(self):
        return "ALPHANUMERIC"


class ALL(WORD):
    """
    This type is WORD, it could contain all characters.
    """

    def __str__(self):
        return "ALL"


class SENTENCE(NONNUMERICAL):
    """
    Sentence is string that ends with fullstops. It could contain spaces.
    """

    def __str__(self):
        return "SENTENCE"


class ARTICLE(NONNUMERICAL):
    """
    Article is string composite from sentences.
    """

    def __str__(self):
        return "ARTICLE"


class PHRASE(NONNUMERICAL):
    """
    Phrase is string with spaces, but it is not sentence.
    """

    def __str__(self):
        return "PHRASE"


class MULTIPLE_VALUES(NONNUMERICAL):
    """
    MULTIPLE_VALUES is string, and it contains pattern that is repeated. (Name1|Name2|Name3|Name4)
    """

    def __str__(self):
        return "MULTIPLE_VALUES"
