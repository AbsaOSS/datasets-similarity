"""
This file contains column2Vec implementations.
"""
import re

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer


def column2vec_as_sentence(column: pd.Series, model: SentenceTransformer):
    """
    Convert a column to a vector

    Make one string from all the items in the column.
    Convert string to a vector by sentence transformer.
    """
    sentence = [str(column.tolist()).replace("\'", "").replace("]", "").replace("[", "")]
    return model.encode(sentence)[0]


def column2vec_as_sentence_clean(column: pd.Series, model: SentenceTransformer):
    """
    Convert a column to a vector

    Make one string from all the items in the column, clean the column that
     it will contain only a-z and 0-9.
    Convert string to a vector by sentence transformer.
    """
    column_as_str = str(column.tolist()).lower()
    sentence = [re.sub("[^(0-9 |a-z)]", " ", column_as_str)]
    return model.encode(sentence)[0]


def column2vec_as_sentence_clean_uniq(column: pd.Series, model: SentenceTransformer):
    """
    Convert a column to a vector

    Make one string from all the items in the column,
    clean the column that it will contain only a-z and
    0-9, it will contain only uniq values.
    Convert string to a vector by sentence transformer.
    """
    uniq_column = column.unique()
    column_as_str = str(uniq_column.tolist()).lower()
    sentence = [re.sub("[^(0-9 |a-z)]", " ", column_as_str)]
    return model.encode(sentence)[0]


def column2vec_avg(column: pd.Series,  model: SentenceTransformer):
    """
    Convert a column to a vector

    Convert each item in the column to a vector and return the average of all the vectors
    """
    uniq_column = column.unique()
    column_clean = pd.Series(uniq_column).apply(lambda x: re.sub("[^(0-9 |a-z)]",
                                                                 " ", str(x).lower())).values
    encoded_columns = model.encode(column_clean)
    to_ret = np.mean(encoded_columns, axis=0)  # counts arithmetic mean (average)
    return to_ret


def column2vec_weighted_avg(column: pd.Series, model: SentenceTransformer):
    """
    Convert a column to a vector

    Convert each item in the column to a vector and return the weighted average of all the vectors
    """
    uniq_column = column.value_counts(normalize=True)
    weights = uniq_column.values
    column_clean = pd.Series(uniq_column.keys()).apply(lambda x: re.sub("[^(0-9 |a-z)]",
                                                                        " ", str(x).lower())).values
    encoded_columns = model.encode(column_clean)
    to_ret = np.average(encoded_columns, axis=0, weights=weights)  # counts weighted average
    return to_ret


def column2vec_sum(column: pd.Series,  model: SentenceTransformer):
    """
    Convert a column to a vector

    Convert each item in the column to a vector and return the average of all the vectors
    """
    uniq_column = column.unique()
    column_clean = pd.Series(uniq_column).apply(lambda x: re.sub("[^(0-9 |a-z)]",
                                                                 " ", str(x).lower())).values
    encoded_columns = model.encode(column_clean)
    to_ret = sum(encoded_columns)  # sum of values
    return to_ret


def column2vec_weighted_sum(column: pd.Series, model: SentenceTransformer):
    """
    Convert a column to a vector

    Convert each item in the column to a vector and return the weighted average of all the vectors
    """
    uniq_column = column.value_counts(normalize=True)
    weights = uniq_column.values
    column_clean = pd.Series(uniq_column.keys()).apply(lambda x: re.sub("[^(0-9 |a-z)]",
                                                                        " ", str(x).lower())).values
    encoded_columns = model.encode(column_clean)
    to_ret = 0
    for number, weight in zip(encoded_columns, weights):
        to_ret += number * weight
    return to_ret
