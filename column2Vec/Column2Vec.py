"""
This file contains column2Vec implementations.
"""
from __future__ import annotations

import json
import re
import logging

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from torch import Tensor

logger = logging.getLogger(__name__)


class Cache:
    """
    Class for cashing column2Vec
    """
    # loaded cache
    __cache = pd.DataFrame()
    # False if the file containing cache was not read yet
    __read_from_file = False
    # enable/disable cache
    __off = False
    # default cache file
    __file = "generated/cache.txt"

    def __read(self):
        try:
            self.__cache = pd.io.parsers.read_csv(self.__file, index_col=0)
        except FileNotFoundError:
            logger.warning("CACHE: File not found.")
        except pd.errors.EmptyDataError:
            logger.warning("CACHE: No data")
        except pd.errors.ParserError:
            logger.warning("CACHE: Parser error")

    def get_cache(self, key: str, function: str) -> list | None:
        """
        It reads cache from file if it is necessary.
         Returns cache for a specific key.
        :param key: Name of colum
        :param function: Name of function
        :return: Cache for a specific key
        """
        if self.__off:
            return None
        if not self.__read_from_file:
            self.__read()
            self.__read_from_file = True
        if function in self.__cache.index and key in self.__cache.columns:
            return json.loads(self.__cache.loc[function, key])  # json is faster than ast
        return None

    def save(self, key: str, function: str, embedding: Tensor | int):
        """
        Saves cache
        :param key: Column name
        :param function: Function name
        :param embedding: to save
        """
        if self.__off:
            return
        self.__cache.loc[function, key] = str(list(embedding))
        # self.__cache.loc[function, key] = embedding

    def save_persistently(self):
        """
        Write cache to csv file
        """
        if self.__off:
            return
        self.__cache.to_csv(self.__file, index=True)

    def off(self):
        """sets off cache"""
        self.__off = True

    def on(self):
        """sets on cache"""
        self.__off = False

    def set_file(self, file: str):
        """sets file for cache"""
        self.__file = file

    def clear_cache(self):
        """clear cache and set read_from_file to False"""
        self.__cache = self.__cache[0:0]
        self.__read_from_file = False

    def clear_persistent_cache(self):
        """clear cache saved in file"""
        try:
            open(self.__file, 'w').close()
        except FileNotFoundError as e:
            print(e)


cache = Cache()


def clean_text(text):
    """ Cleans text, removes all characters except a-z and 0-9 """
    return re.sub("[^(0-9 |a-z)]", " ", str(text).lower())


def column2vec_as_sentence(column: pd.Series, model: SentenceTransformer, key: str) -> Tensor:
    """
    Convert a column to a vector

    Make one string from all the items in the column
    Convert string to a vector by sentence transformer.
    :param column: to be transformed
    :param model: for transforming to embedding
    :param key: for saving to cache (exmp. name of column)
    """
    function_string = "column2vec_as_sentence"
    res = cache.get_cache(key, function_string)
    if res is not None:
        return res

    sentence = [str(column.tolist()).replace("\'", "").replace("]", "").replace("[", "")]
    embedding = model.encode(sentence)[0]

    cache.save(key, function_string, embedding)
    return embedding


def column2vec_as_sentence_clean(column: pd.Series, model: SentenceTransformer, key: str):
    """
    Convert a column to a vector

    Make one string from all the items in the column, clean the column that
     it will contain only a-z and 0-9.
    Convert string to a vector by sentence transformer.

    :param column: to be transformed
    :param model: for transforming to embedding
    :param key: for saving to cache (exmp. name of column)
    """
    function_string = "column2vec_as_sentence_clean"
    res = cache.get_cache(key, function_string)
    if res is not None:
        return res

    column_as_str = str(column.tolist()).lower()
    sentence = [re.sub("[^(0-9 |a-z)]", " ", column_as_str)]
    embedding = model.encode(sentence)[0]

    cache.save(key, function_string, embedding)
    return embedding


def column2vec_as_sentence_clean_uniq(column: pd.Series, model: SentenceTransformer, key: str):
    """
    Convert a column to a vector

    Make one string from all the items in the column,
    clean the column that it will contain only a-z and
    0-9, it will contain only uniq values.
    Convert string to a vector by sentence transformer.

    :param column: to be transformed
    :param model: for transforming to embedding
    :param key: for saving to cache (exmp. name of column)
    """
    function_string = "column2vec_as_sentence_clean_uniq"
    res = cache.get_cache(key, function_string)
    if res is not None:
        return res

    uniq_column = column.unique()
    column_as_str = str(uniq_column.tolist()).lower()
    sentence = [re.sub("[^(0-9 |a-z)]", " ", column_as_str)]

    embedding = model.encode(sentence)[0]

    cache.save(key, function_string, embedding)
    return embedding


def weighted_create_embed(column: pd.Series, model: SentenceTransformer, key: str,
                          function_string: str) -> tuple[list, list]:
    """
    Creates embedding, it could be used for both weighted impl.
    :param column: to be embedded
    :param model: to transform
    :param key: name of column
    :param function_string:  name of function
    :return: embeddings and weights
    """
    res = cache.get_cache(key, function_string)
    if res is not None:
        return res, None

    uniq_column = column.value_counts(normalize=True)
    weights = uniq_column.values
    column_clean = pd.Series(uniq_column.keys()).apply(clean_text).values
    return model.encode(column_clean), weights


def column2vec_avg(column: pd.Series, model: SentenceTransformer, key: str):
    """
    Convert a column to a vector

    Convert each item in the column to a vector and return the average of all the vectors

    :param column: to be transformed
    :param model: for transforming to embedding
    :param key: for saving to cache (exmp. name of column)
    """
    function_string = "column2vec_avg"
    res = cache.get_cache(key, function_string)
    if res is not None:
        return res
    uniq_column = column.unique()
    column_clean = pd.Series(uniq_column).apply(clean_text).values
    encoded_columns = model.encode(column_clean)
    to_ret = np.mean(encoded_columns, axis=0)  # counts arithmetic mean (average)
    cache.save(key, function_string, to_ret)
    return to_ret


def column2vec_weighted_avg(column: pd.Series, model: SentenceTransformer, key: str):
    """
    Convert a column to a vector

    Convert each item in the column to a vector and return the weighted average of all the vectors

    :param column: to be transformed
    :param model: for transforming to embedding
    :param key: for saving to cache (exmp. name of column)
    """
    function_string = "column2vec_weighted_avg"
    res = cache.get_cache(key, function_string)
    if res is not None:
        return res
    uniq_column = column.value_counts(normalize=True)
    weights = uniq_column.values
    column_clean = pd.Series(uniq_column.keys()).apply(clean_text).values
    res = model.encode(column_clean)

    # encoded_columns, weights = weighted_create_embed(column, model, key, function_string)
    to_ret = np.average(res, axis=0, weights=weights)  # counts weighted average
    cache.save(key, function_string, to_ret)
    return to_ret


def column2vec_sum(column: pd.Series, model: SentenceTransformer, key: str):
    """
    Convert a column to a vector

    Convert each item in the column to a vector and return the average of all the vectors

    :param column: to be transformed
    :param model: for transforming to embedding
    :param key: for saving to cache (exmp. name of column)
    """
    function_string = "column2vec_sum"
    res = cache.get_cache(key, function_string)
    if res is not None:
        return res

    uniq_column = column.unique()
    column_clean = pd.Series(uniq_column).apply(clean_text).values.tolist()
    encoded_columns = model.encode(column_clean)
    to_ret = sum(encoded_columns)  # sum of values
    cache.save(key, function_string, to_ret)  # todo
    return to_ret


def column2vec_weighted_sum(column: pd.Series, model: SentenceTransformer, key: str):
    """
    Convert a column to a vector.

    Convert each item in the column to a vector and return the weighted average of all the vectors.

    :param column: to be transformed
    :param model: for transforming to embedding
    :param key: for saving to cache (exmp. name of column)
    """
    function_string = "column2vec_weighted_sum"
    encoded_columns, weights = weighted_create_embed(column, model, key, function_string)
    if weights is None:
        return encoded_columns
    to_ret = 0
    for number, weight in zip(encoded_columns, weights):
        to_ret += number * weight
    cache.save(key, function_string, to_ret)  # todo
    return to_ret
