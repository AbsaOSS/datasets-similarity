import math
import re
from itertools import compress

import numpy as np
import pandas as pd
from typing import Optional
from sentence_transformers import SentenceTransformer

from similarity.DataFrameMetadata import DataFrameMetadata, CategoricalMetadata, KindMetadata, NumericalMetadata, \
    NonnumericalMetadata
from similarity.Types import get_basic_type, get_advanced_type, get_advanced_structural_type, get_data_kind, \
    DataKind, series_to_numeric, Type, NUMERICAL, NONNUMERICAL, UNDEFINED, WORD, ALL, MULTIPLE_VALUES, PHRASE, ARTICLE, \
    ALPHANUMERIC, ALPHABETIC


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
        self.model: Optional[SentenceTransformer] = SentenceTransformer('bert-base-nli-mean-tokens')
        self.metadata.size = dataframe.shape[0]
        self.metadata.column_names = list(dataframe.columns)
        self.metadata.column_names_clean = [re.sub("[^(0-9 | a-z).]", " ", i.lower()) for i in
                                            self.metadata.column_names]

        self.metadata.column_incomplete = [i < self.metadata.size * 0.7 for i in
                                           dataframe.count()]  # more than 30 % missing

        # todo correlated column
        # -----------------------------------------------------------------------------------

    def __normalize(self, num1: int, num2: int) -> tuple[int, int]:
        gcd = math.gcd(num1, num2)
        return int(num1 / gcd), int(num2 / gcd)

    def __compute_kind_metadata(self, kind: DataKind, column: pd.Series) -> KindMetadata:
        if kind == DataKind.BOOL:
            count = column.value_counts()
            null_values = True if len(column) != count.iloc[0] + count.iloc[1] else False
            return KindMetadata(tuple([count.keys()[0], count.keys()[1]]),
                                self.__normalize(count.iloc[0], count.iloc[1]),
                                None, None, null_values)
        if kind == DataKind.ID:
            null_values = True if column.nunique() != len(column) else False
            longest = column[column.apply(str).map(len).argmax()]
            shortest = column[column.apply(str).map(len).argmin()]
            return KindMetadata(None, None, longest, shortest, null_values)
        if kind == DataKind.CONSTANT:
            count = column.value_counts().iloc[0]
            length = len(column)
            if length != count:
                return KindMetadata(tuple([column.dropna().unique()[0]]), self.__normalize(count, length - count),
                                    None, None, True)
            else:
                return KindMetadata(tuple(column.dropna().unique()[0], ), None, None, None, False)

    def __compute_type_metadata(self, type_: Types, column: pd.Series, name: str) -> None:
        """
        Compute metadata for numerical and nonnumerical columns
        column.str.len().nunique() == 1 returns len for each element in series, then we count number of uniq values
        -> how many elements have the same length

        :param type_: of column
        :param column: the specific column
        :param name: name of the column
        :return: None
        """
        if issubclass(type_, NUMERICAL):
            column = series_to_numeric(column)
            self.metadata.numerical_metadata[name] = NumericalMetadata(
                column.min(), column.max(), (column.astype(str).str.len().nunique() == 1)
            )
        elif issubclass(type_, NONNUMERICAL):
            self.metadata.nonnumerical_metadata[name] = NonnumericalMetadata(
                column[column.astype(str).str.len().idxmax()],  # longest string
                column[column.astype(str).str.len().idxmin()],  # shortest string
                int(column.astype(str).str.len().mean())
            )

    def __get_model(self) -> SentenceTransformer:
        """
        :return: embedding model if exists or creates new one
        """
        if not self.model:
            self.model = SentenceTransformer('bert-base-nli-mean-tokens')
        return self.model

    ## Setting Creator

    def set_model(self, model: SentenceTransformer) -> 'DataFrameMetadataCreator':
        """
        Sets model
        :param model: to be set
        :return: self DataFrameMetadataCreator
        """
        self.model = model
        return self

    def compute_column_names_embeddings(self) -> 'DataFrameMetadataCreator':
        """
        Computes embeddings for all column names

        :return: self
        """
        column_name_embeddings = self.__get_model().encode(self.metadata.column_names_clean)
        for i, name in zip(column_name_embeddings, self.metadata.column_names):
            self.metadata.column_name_embeddings[name] = i
        return self

    def compute_column_kind(self) -> 'DataFrameMetadataCreator':
        """
        This will compute columns kinds (id, bool, undefined, constant, categorical) and kind metadata
        and categorical metadata

        :return: self
        """
        for i in self.dataframe.columns:
            kind = get_data_kind(self.dataframe[i])
            self.metadata.column_kind[kind].add(i)
            self.metadata.kind_metadata[i] = self.__compute_kind_metadata(kind, self.dataframe[i])
            if kind == DataKind.CATEGORICAL:
                self.metadata.categorical_metadata[i] = \
                    CategoricalMetadata(count=self.dataframe[i].nunique(),
                                        categories=list(self.dataframe[i].unique()),
                                        categories_with_count=self.dataframe[i].value_counts(),
                                        category_embedding=self.__get_model().encode(
                                            list(map(str, self.dataframe[i].unique()
                                                     ))))

        return self

    def compute_basic_types(self) -> 'DataFrameMetadataCreator':
        """
        Computes types of columns only numerical, date, not numerical and undefined
        computes metadata

        :return: self
        """
        for i in self.dataframe.columns:
            type_ = get_basic_type(self.dataframe[i])
            self.metadata.type_column[type_].add(i)
            self.__compute_type_metadata(type_, self.dataframe[i], i)
        return self

    def compute_advanced_types(self) -> 'DataFrameMetadataCreator':
        """
        Computes types of columns. Indicates types int, float, date, text
        computes metadata

        :return: self
        """
        for i in self.dataframe.columns:
            type_ = get_advanced_type(self.dataframe[i])
            self.metadata.type_column[type_].add(i)
            self.__compute_type_metadata(type_, self.dataframe[i], i)
        return self

    def compute_advanced_structural_types(self) -> 'DataFrameMetadataCreator':
        """
        Compute types of columns. Indicates type of column int, float - human, computer, date, text - word, sentence, phrase article, multiple
        computes metadata

        :return: self
        """
        for i in self.dataframe.columns:
            type_ = get_advanced_structural_type(self.dataframe[i])
            self.metadata.type_column[type_].add(i)
            self.__compute_type_metadata(type_, self.dataframe[i], i)
        return self

    def compute_correlation(self, strong_correlation: float) -> 'DataFrameMetadataCreator':
        """
        todo
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
            types = [NONNUMERICAL, UNDEFINED, WORD, ALL, MULTIPLE_VALUES, PHRASE, ARTICLE, ALPHANUMERIC, ALPHABETIC ] ## todo
        sentences = []
        names = []
        for i in types:
            for column in self.metadata.type_column[i]:
                sentences.append(str(self.dataframe[column].tolist())
                                 .replace("\'", "")
                                 .replace("]", "")
                                 .replace("[", ""))  # column to string
                names.append(column)
        column_embeddings = self.__get_model().encode(sentences)
        for i, name in zip(column_embeddings, names):
            self.metadata.column_embeddings[name] = i
        return self

    ## Getters
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
