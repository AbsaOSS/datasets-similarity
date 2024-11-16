import logging

import numpy as np
import pandas as pd
from torch import Tensor

from src.models.constants import warning_enable


def concat(self, *data_frames: pd.DataFrame) -> pd.DataFrame:
    """
    Concat all dataframes together, compute avg for each cell
    :param data_frames: array of dataframes
    :return: new dataframe
    """
    res = data_frames[0]
    for d in data_frames[1:]:
        res = res.add(d)
    return res.map(lambda x: x / len(data_frames))


def cosine_sim(u: list | Tensor, v: list | Tensor) -> float:  # todo move to functions.py?
    """
    Compute cosine similarity (range 0 to 1) 1 teh same 0 completely different
    :param u: embeddings 1
    :param v: embeddings 2
    :return:
    """
    return round(
        np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v)),
        3,
    )  # todo change rounding to 4, 5 6 ...etc


def get_ratio(count1: int, count2: int) -> float:
    """
    Compute ratio between two numbers. If one of the numbers is 0 return 1. Ratio is between 1 and 0.
    :param count1: number 1
    :param count2: number 2
    :return: ratio between 0 and 1
    """
    if count1 == 0 or count2 == 0:
        return 1
    if count1 < count2:
        return count2 / count1
    return count1 / count2


def fill_result(metadata1_names, metadata2_names) -> pd.DataFrame:
    """
    Fill result with 0 if the names are the same, otherwise fill with 1
    """
    result = pd.DataFrame()
    for idx1, name1 in enumerate(metadata1_names.values()):
        for idx2, name2 in enumerate(metadata2_names.values()):
            result.loc[idx1, idx2] = 0 if name1 == name2 else 1
    return result


def are_columns_null(column1: set, column2: set, message: str) -> tuple[bool, float]:
    """
    Check if columns are empty
    :param column1: to be compared
    :param column2: to be compared
    :param message: kind type
    :return:  tuple of bool and float, if columns are empty return True
    """
    if len(column1) == 0 and len(column2) == 0:
        if warning_enable.get_status():
            logging.info(f"Warning: {message} is not present in the dataframe.")
        return True, 0
    if (len(column1) == 0) != (len(column2) == 0):
        if warning_enable.get_status():
            logging.info(f"Warning: {message} is not present in one of the dataframes.")
        return True, 1
    return False, 0
