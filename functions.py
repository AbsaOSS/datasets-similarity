import math
from collections import defaultdict
from itertools import compress

from DataFrameMetadata import DataFrameMetadata, CategoricalMetadata
from Types import Types
from typing import Optional

import pandas as pd
import numpy as np
import os
import re
from sentence_transformers import SentenceTransformer
import gensim.downloader as api


def get_world_embedding(world):
    # takes 3-10 minutes to load
    global wv
    if not wv:
        wv = api.load('word2vec-google-news-300')
    return wv[world]


sbert_model: Optional[SentenceTransformer] = None


def get_sbert_model() -> SentenceTransformer:
    global sbert_model
    if not sbert_model:
        sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')
    return sbert_model


def load__csv_files_from_folder(folder: str) -> (list[pd.DataFrame], list[str]):
    """
    it loads cvs files from folder and returns list of loaded dataframe and list of names
    :param folder: from which we load the files
    :return: two lists
    """
    data = []
    names = []
    for file in os.listdir(folder):
        if file.endswith(".csv"):
            data.append(pd.read_csv(folder + "/" + file))
            names.append(file.replace(".csv", ""))
    return data, names


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


def is_bool(column: pd.Series) -> bool:
    """
    Decide if type is bool
    :param column:
    :return: True if type is boolean
    """
    if np.issubdtype(column.dtype, np.bool_):
        return True
    return type(column.mode()[0]) is bool


## todo make better more accurate
## TODO switch
def get_type(column: pd.Series) -> Types:
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


def create_string_from_columns(database: list[pd.DataFrame], table_names: list[str]) -> (list[str], list[str]):
    """
    For each column in each table in database it creates string from that column.
    :param database: all tables
    :param table_names: all names of tables
    :return: list of strings representing column, list of string of the same length representing names of table for each column
    """
    sentences = []
    sentences_datasets = []
    for table, name in zip(database, table_names):
        for column in table.columns:
            sentences.append(
                str(table[column].tolist()).replace("\'", "").replace("]", "").replace("[", ""))  # column to string
            sentences_datasets.append(name)
    return sentences, sentences_datasets


class DataFrameMetadataCreator:
    """
    This class gets dataframe and creates metadata.
    Specific metadata will be created after calling specific function.
    User will get created metadata by calling get_metadata()
    """
    ## generated by computer/person
    ## distribution of numerical data
    ## most common triplets, ... for text data
    ##
    def __init__(self, dataframe: pd.DataFrame):
        """
        Constructor of DataFrameMetadataCreator
        :param dataframe: DataFrame from which we will create metadata

        size of metadata will be set to number of DataFrames rows
        column_names_clean will be set to column names with only letters and numbers
        column_name_embeddings will be created by using vector embedding model
        type_column - each type will have list of names of columns with this specific type
        column_categorical - list of booleans, for each column list will contain
                            True for categorical data and False for not categorical
        column_incomplete - list of booleans, for each column list will contain
                            True for incomplete data and False otherwise
        """
        self.dataframe = dataframe
        self.metadata = DataFrameMetadata()
        self.metadata.size = dataframe.shape[0]
        self.metadata.column_names = list(dataframe.columns)
        self.metadata.column_names_clean = [re.sub("[^(0-9 | a-z).]", " ", i.lower()) for i in
                                            self.metadata.column_names]
        self.metadata.column_name_embeddings = get_sbert_model().encode(self.metadata.column_names_clean)
        for i in dataframe.columns:
            self.metadata.type_column[get_type(dataframe[i])].add(i)

        self.metadata.column_categorical = [((i / (self.metadata.size * 0.01) < 1) or i < 50) for i in
                                            dataframe.nunique()]  # less than 10 %
        self.metadata.column_incomplete = [i < self.metadata.size * 0.7 for i in
                                           dataframe.count()]  # more than 30 % missing
        self.__compute_categorical_info()

    def __compute_categorical_info(self) -> None:
        """
        Method creates CategoricalMetadata

        """
        categorical_names = list(compress(self.metadata.column_names, self.metadata.column_categorical))
        for name in categorical_names:
            # clean_categories = self.dataframe[name].notna().unique()
            # categories_embeddings = list()
            # for category in clean_categories:
            #     get_world_embedding(category)
            if name in self.metadata.type_column[Types.BOOL]:
                continue
            self.metadata.categorical_metadata[name] = CategoricalMetadata(count=self.dataframe[name].nunique(),
                                                                           categories=set(
                                                                               self.dataframe[name].unique()),
                                                                           categories_with_count=self.dataframe[
                                                                               name].value_counts(),
                                                                           category_embedding=get_sbert_model().encode(list(map(str, self.dataframe[name].unique()))))
            # categories_embeddings=categories_embeddings)

    def compute_correlation(self, strong_correlation: float) -> 'DataFrameMetadataCreator':
        """
        Compute correlation for numerical columns and saves it to correlated_columns as tuple of correlation number and name of column
        :param strong_correlation: threshold for deciding if two columns are correlated
        :return: self DataFrameMetadataCreator
        """
        correlation_numerical = self.get_numerical_columns().corr()
        res = [(i, j) for i, j in zip(*np.where(np.abs(correlation_numerical.values) > strong_correlation))
               if i != j]  ## get pairs from matrics with bigger value then strong_correlation
        for r in res:
            self.metadata.correlated_columns.add(
                tuple(sorted((correlation_numerical.columns[r[0]],
                              correlation_numerical.iloc[r[1]].name))))  ## get names of rows and columns
        return self

    def create_column_embeddings(self, types=None) -> 'DataFrameMetadataCreator':
        """
        Creates embeddings for Types.STRING, Types.TEXT, Types.UNDEFINED or another types according to types parameter

        :param types: optional parameter for set desirable types
        :return: self DataFrameMetadataCreator
        """
        if types is None:
            types = [Types.STRING, Types.TEXT, Types.UNDEFINED]
        sentences = []
        names = []
        for i in types:
            for column in self.metadata.type_column[i]:
                sentences.append(str(self.dataframe[column].tolist())
                                 .replace("\'", "")
                                 .replace("]", "")
                                 .replace("[", ""))  # column to string
                names.append(column)
        column_embeddings = get_sbert_model().encode(sentences)
        for i, name in zip(column_embeddings, names):
            self.metadata.column_embeddings[name] = i
        return self

    def get_column_by_type(self, *types):
        """
        :param types: of columns
        :return: dataframe with columns with specific types
        """
        return self.dataframe[self.metadata.get_column_names_by_type(types)]

    def get_numerical_columns(self):
        """
        :return: dataframe with only numerical columns
        """
        return self.dataframe[self.metadata.get_numerical_columns_names()]

    def get_metadata(self) -> DataFrameMetadata:
        """
        :return: created metadata
        """
        return self.metadata
