import re
from enum import Enum

import numpy as np
import pandas as pd


def is_bool(column: pd.Series) -> bool:
    """
    Decide if type is bool
    :param column:
    :return: True if type is boolean
    """
    if np.issubdtype(column.dtype, np.bool_):
        return True
    return type(column.mode()[0]) is bool


def is_numerical(x) -> bool:
    """
    Decide if np type is numerical
    :param x: the type
    :return: true if it is numerical, otherwise false
    """
    return np.issubdtype(x, np.integer) or np.issubdtype(x, np.floating)


def is_date(column: pd.Series) -> bool:
    """
    Decide if type of column is date
    :param column:
    :return:
    """
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


## todo make better more accurate
## TODO switch
def get_type(column: pd.Series) -> 'Types':
    """
    Indicates type of column.

    :param column: to indicate
    :return: detected type
    """
    if is_numerical(column.dtype):
        return Types.NUMERICAL
    if np.issubdtype(column.dtype, np.integer):
        return Types.INT
    if np.issubdtype(column.dtype, np.floating):
        return Types.FLOAT
    if is_bool(column):
        return Types.BOOL  # todo test this
    if is_date(column):
        return Types.DATE
    if is_string(column):
        return Types.STRING
    if is_text(column):
        return Types.TEXT
    else:
        return Types.UNDEFINED

class Types(Enum):
    """
    Enum class representing column type
    """
    NUMERICAL = 1
    INT = 5
    FLOAT = 6
    BOOL = 8
    DATE = 7
    STRING = 3
    TEXT = 4
    UNDEFINED = 0
