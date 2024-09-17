"""
File contains Comparator class, ComparatorType classes and DistanceFunction class.
Comparator is split to types comparator, all columns with same types are compare together
"""
from __future__ import annotations

import math
import warnings
from abc import abstractmethod, ABC
from enum import Enum
from statistics import mean

import numpy as np
import pandas as pd
from torch import Tensor

from similarity.DataFrameMetadata import DataFrameMetadata
from similarity.Types import DataKind
from constants import warning_enable


class Settings(Enum):
    """Settings enum, if we want to use embeddings for columns, ratio between different comparators"""
    EMBEDDINGS = 1
    NO_RATIO = 2


def cosine_sim(u: list | Tensor, v: list | Tensor) -> float:  # todo move to functions.py?
    """
    Compute cosine similarity (range 0 to 1) 1 teh same 0 completely different
    :param u: embeddings 1
    :param v: embeddings 2
    :return:
    """
    return round(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v)), 3)  # todo change rounding to 4, 5 6 ...etc


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


class DistanceFunction(ABC):
    """Abstract class for distance classes"""

    @abstractmethod
    def compute(self, distance_table: pd.DataFrame):
        """Method should compute overall distance from distance_table"""


class HausdorffDistanceMin(DistanceFunction):
    """Hausdorff distance class"""

    def compute(self, distance_table: pd.DataFrame) -> float:
        """
        Compute Hausdorff distance with min function.
        :param distance_table:  dataframe
        :return: float between 0 and 1
        """
        if distance_table.size == 0:
            return np.nan
        row_mins = distance_table.min(axis=1)
        column_mins = distance_table.min(axis=0)
        return min(row_mins.max(), column_mins.max())


class ComparatorType(ABC):
    """Abstract class for comparators"""

    def __init__(self, weight: int = 1):
        """
        Constructor for ComparatorType
        :param weight: weight of the comparator
        """
        self.weight = weight

    @abstractmethod
    def compare(self, metadata1: DataFrameMetadata, metadata2: DataFrameMetadata,
                distance_function: DistanceFunction, settings: set[Settings]) -> pd.DataFrame:
        """This method should compare two tables and return distance table"""

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


class CategoricalComparator(ComparatorType):
    """
    Categorical comparator class
    """

    def __compute_distance(self, dist_matrix: list[list[float]]) -> float:  # Hausdorff
        """
        Compute distance from similarity matrix
        todo maybe switch to hausdorfdist??
        """
        row_mins = []
        column_mins = []
        for row in dist_matrix:
            row_mins.append(min(row))
        for column in zip(*dist_matrix):
            column_mins.append(min(column))
        return min([max(row_mins), max(column_mins)])

    def __create_dist_matrix(self, embeddings1: list[Tensor], embeddings2: list[Tensor]) -> list[list[float]]:
        """
        creates similarity matrix for embeddings
        :param embeddings1: embeddings for first column
        :param embeddings2: embeddings for second column
        :return: similarity matrix
        """
        simil_matrix = []
        for embed1 in embeddings1:
            siml_line = []
            for embed2 in embeddings2:
                # todo rounding for 3 digits ? ok -> two because of minus 0
                siml_line.append(round(1 - round(cosine_sim(embed1, embed2), 4), 3))  # distance is 1- similarity
            simil_matrix.append(siml_line)
        return simil_matrix

    def compare(self, metadata1: DataFrameMetadata, metadata2: DataFrameMetadata, distance_function: DistanceFunction,
                settings: set[Settings]) -> pd.DataFrame:
        """
        Compare two categorical columns
         the distance is between 0 and 1
        :param distance_function: - not used
        :param metadata1: first table
        :param metadata2: second table
        :param settings: - not used
        :return: dataframe full of numbers between 0 and 1
        """
        result = pd.DataFrame()
        name_distance = pd.DataFrame()
        for id1, (column1, categorical1) in enumerate(metadata1.categorical_metadata.items()):
            for id2, (column2, categorical2) in enumerate(metadata2.categorical_metadata.items()):
                simil_matrix = self.__create_dist_matrix(categorical1.category_embedding,
                                                         categorical2.category_embedding)
                # count, score = self.__compute_similarity_score(simil_matrix)
                dist = self.__compute_distance(simil_matrix)
                ratio = get_ratio(categorical1.count_categories, categorical1.count_categories)
                result.loc[id1, id2] = dist * ratio
                name_distance.loc[id1, id2] = 1 - cosine_sim(metadata1.column_name_embeddings[column1],
                                                             metadata2.column_name_embeddings[column2])
        # todo p value or correlation
        return self.concat(result, name_distance)


class CategoricalComparatorSimilar(CategoricalComparator):
    """
    Comparator for column category
    """

    def __create_sim_matrix(self, embeddings1: list[Tensor], embeddings2: list[Tensor]) -> list[list[float]]:
        simil_matrix = []
        for embed1 in embeddings1:
            siml_line = []
            for embed2 in embeddings2:
                siml_line.append(round(cosine_sim(embed1, embed2), 3))
            simil_matrix.append(siml_line)
        return simil_matrix

    def __compute_similarity_score(self, similarity_matrix: list[list[float]]) -> tuple[
        int, float]:  # todo test some other methods
        # todo use Haufsdorfe distance ?
        res = 0.0
        count = 0
        trashold = 0.7  # todo set from outside
        for i in similarity_matrix:
            if max(i) > trashold:
                count += 1
            res += max(i)
        return count, res / len(similarity_matrix) * (count / len(similarity_matrix))

    def compare(self, metadata1: DataFrameMetadata, metadata2: DataFrameMetadata, distance_function: DistanceFunction,
                settings: set[Settings]) -> pd.DataFrame:
        """
        Compare categorical columns, if the columns are similar
        :param distance_function: - not used
        :param metadata1: first table
        :param metadata2: second table
        :param settings: - not used
        :return: dataframe full of numbers between 0 and 1
        """
        result = pd.DataFrame()
        name_distance = pd.DataFrame()
        for id1, (column1, categorical1) in enumerate(metadata1.categorical_metadata.items()):
            for id2, (column2, categorical2) in enumerate(metadata2.categorical_metadata.items()):
                simil_matrix = self.__create_sim_matrix(categorical1.category_embedding,
                                                        categorical2.category_embedding)
                _, score = self.__compute_similarity_score(simil_matrix)
                ratio = get_ratio(categorical1.count_categories, categorical1.count_categories)  # todo 1-ratio???
                result.loc[id1, id2] = 1 - (score * ratio)
                name_distance.loc[id1, id2] = 1 - cosine_sim(metadata1.column_name_embeddings[column1],
                                                             metadata2.column_name_embeddings[column2])
        # todo p value or correlation
        return self.concat(result, name_distance)


class ColumnEmbeddingComparator(ComparatorType):
    """
    Comparator for column values embeddings
    """

    def compare(self, metadata1: DataFrameMetadata, metadata2: DataFrameMetadata, distance_function: DistanceFunction,
                settings: set[Settings]) -> pd.DataFrame:
        """
        Compare embeddings of columns
        :param distance_function: - not used
        :param metadata1: first table
        :param metadata2: second table
        :param settings: - not used
        :return: dataframe full of numbers between 0 and 1
        """
        result = pd.DataFrame()
        name_distance = pd.DataFrame()
        for id1, (column1, embedding1) in enumerate(metadata1.column_embeddings.items()):
            for id2, (column2, embedding2) in enumerate(metadata2.column_embeddings.items()):
                result.loc[id1, id2] = 1 - cosine_sim(embedding1, embedding2)
                name_distance.loc[id1, id2] = 1 - cosine_sim(metadata1.column_name_embeddings[column1],
                                                             metadata2.column_name_embeddings[column2])
        return self.concat(result, name_distance)


class SizeComparator(ComparatorType):
    """
    Size of table comparator class
    """

    def compare(self, metadata1: DataFrameMetadata, metadata2: DataFrameMetadata, distance_function: DistanceFunction,
                settings: set[Settings]) -> pd.DataFrame:
        """
        If sizes are the same distance is 0, else distance is 1 - % of max
        :param distance_function: - not used
        :param metadata1: first table
        :param metadata2: second table
        :param settings: - not used
        :return: dataframe of size 1x1 fill with distance number (0-1) # todo test
        """
        max_size = int(max(metadata1.size, metadata2.size))
        min_size = int(min(metadata1.size, metadata2.size))
        distance = 1 - (min_size / max_size)
        return pd.DataFrame(index=range(1), columns=range(1)).fillna(distance)
        # todo if this is not working try this We will fill the whole table with this numer, distance function should compute the same number (todo test)


def fill_result(metadata1_names, metadata2_names) -> pd.DataFrame:
    """
    Fill result with 0 if the names are the same, otherwise fill with 1
    """
    result = pd.DataFrame()
    for idx1, name1 in enumerate(metadata1_names.values()):
        for idx2, name2 in enumerate(metadata2_names.values()):
            result.loc[idx1, idx2] = 0 if name1 == name2 else 1
    return result


class ColumnExactNamesComparator(ComparatorType):
    """
    Comparator for exact column names
    """

    def compare(self, metadata1: DataFrameMetadata, metadata2: DataFrameMetadata, distance_function: DistanceFunction,
                settings: set[Settings]) -> pd.DataFrame:
        """
        This is dummy comparator if the names are exactly the same distance is 0 if not distance is 1
        :param distance_function: - not used
        :param metadata1: first table
        :param metadata2: second table
        :param settings: - not used
        :return: dataframe fill by 0 and 1
        """
        if (metadata1.column_names_clean == {} or metadata2.column_names_clean == {}) and warning_enable.get_status():
            warnings.warn("Warning: column_names_clean is not computed")
        return fill_result(metadata1.column_names_clean, metadata2.column_names_clean)


class ColumnNamesEmbeddingsComparator(ComparatorType):
    """
    Comparator for column names embeddings
    """

    def compare(self, metadata1: DataFrameMetadata, metadata2: DataFrameMetadata, distance_function: DistanceFunction,
                settings: set[Settings]) -> pd.DataFrame:
        """
        Computes cosine distance for each column name embedding
        :param distance_function: - not used
        :param metadata1: first table
        :param metadata2: second table
        :param settings: - not used
        :return: dataframe fill by distances between 0 and 1
        """
        if (metadata1.column_name_embeddings == {} or metadata2.column_name_embeddings == {}) and warning_enable.get_status():
            warnings.warn("Warning: column name embedding is not computed")

        result = pd.DataFrame()
        for idx1, name1 in enumerate(metadata1.column_name_embeddings.values()):
            for idx2, name2 in enumerate(metadata2.column_name_embeddings.values()):
                result.loc[idx1, idx2] = 1 - cosine_sim(name1, name2)
        return result


class IncompleteColumnsComparator(ComparatorType):
    """
    Comparator for incomplete columns
    """

    def compare(self, metadata1: DataFrameMetadata, metadata2: DataFrameMetadata, distance_function: DistanceFunction,
                settings: set[Settings]) -> pd.DataFrame:
        """
        Compare if two columns are complete or incomplete, if both have same outcome (True False)
         the distance is 0 otherwise is 1
        :param distance_function: - not used
        :param metadata1: first table
        :param metadata2: second table
        :param settings: - not used
        :return: dataframe full of 1 and 0
        """
        return fill_result(metadata1.column_incomplete, metadata2.column_incomplete)



class KindComparator(ComparatorType):
    """
    Comparator for column kind
    """

    def __init__(self, compare_kind=None, weight: dict[DataKind.BOOL, int] = None):
        super().__init__(weight=1)
        if compare_kind is None:
            self.compare_kind = [DataKind.BOOL, DataKind.ID, DataKind.CATEGORICAL, DataKind.CONSTANT]
        else:
            self.compare_kind = compare_kind
        if weight is None:
            self.kind_weight: dict = {DataKind.BOOL: 1, DataKind.ID: 1, DataKind.CATEGORICAL: 1, DataKind.CONSTANT: 1}
        else:
            self.kind_weight = weight

    def compute_result(self, distance_table: pd.DataFrame, distance_function: DistanceFunction, settings: set[Settings],
                       weight: int):
        """
        Compute result from distance table
        """
        tmp = pow(distance_function.compute(distance_table), 2) * weight
        if Settings.NO_RATIO not in settings:
            tmp = tmp * get_ratio(distance_table.shape[0], distance_table.shape[1])
        return tmp

    def compute_embeddings_distance(self, embeddings1, embeddings2) -> float:
        """
        Creates table of distances between embeddings for each row  and computes mean
         of row and column minimums then pick max.
        :param embeddings1: values for column1
        :param embeddings2: values for column2
        :return: float from 0 to 1
        """
        res = []
        row_mins = []
        id1 = 0
        for embed1 in embeddings1:
            results = []
            for embed2 in embeddings2:
                result = 1 - cosine_sim(embed1, embed2)
                results.append(result)
            res.append(results)
            row_mins.append(min(results))
            id1 += 1
        column_mins = []
        for_iter = pd.DataFrame(data=res)
        for _, column in for_iter.items():
            column_mins.append(min(column))
        return max([mean(column_mins), mean(row_mins)])  # todo vysvetlit v textu

    def __are_columns_null(self, column1: set, column2: set, message: str) -> tuple[bool, pd.DataFrame]:
        """
        Check if columns are empty
        :param column1:
        :param column2:
        :param message:
        :return:  tuple of bool and dataframe, if columns are empty return True
        """
        if len(column1) == 0 and len(column2) == 0:
            if warning_enable.get_status():
                warnings.warn(f"Warning: {message} is not present in the dataframe.")
            return True, pd.DataFrame([0])
        if (len(column1) == 0) != (len(column2) == 0):
            if warning_enable.get_status():
                warnings.warn(f"Warning: {message} is not present in one of the dataframes.")
            return True, pd.DataFrame([1])
        return False, pd.DataFrame()

    def compare_constants(self, metadata1: DataFrameMetadata, metadata2: DataFrameMetadata) -> pd.DataFrame:
        """
        Compare all constant columns. Compare if they contain nulls.
        Compare embeddings of values.
        Make an average of these values.
        :param metadata1: for column1
        :param metadata2: for column2
        :return: matrix containing float numbers in range <0, 1>
        """
        value_re = pd.DataFrame()
        nulls_re = pd.DataFrame()
        are_nulls = self.__are_columns_null(metadata1.column_kind[DataKind.CONSTANT],
                                            metadata2.column_kind[DataKind.CONSTANT], "Constant metadata")
        if are_nulls[0]:
            return are_nulls[1]
        for column1 in metadata1.column_kind[DataKind.CONSTANT]:
            for column2 in metadata2.column_kind[DataKind.CONSTANT]:
                # Extract metadata for columns
                meta1 = metadata1.kind_metadata[column1]
                meta2 = metadata2.kind_metadata[column2]

                if meta1.value_embeddings is None or meta2.value_embeddings is None:
                    # 0 distance if values are the same otherwise 1
                    value_re.loc[column1, column2] = int(meta1.value != meta2.value)
                else:
                    value_re.loc[column1, column2] = 1 - cosine_sim(meta1.value_embeddings, meta2.value_embeddings)

                # 0 distance if values are the same otherwise 1
                nulls_re.loc[column1, column2] = int(meta1.nulls != meta2.nulls)

                # if nulls are equal and exist
                if nulls_re.loc[column1, column2] == 0 and meta1.nulls:
                    ratio1 = meta1.distribution[0] / meta1.distribution[1]
                    ratio2 = meta2.distribution[0] / meta2.distribution[1]
                    nulls_re.loc[column1, column2] = abs(ratio1 - ratio2)  # compute difference between distribution

        return self.concat(nulls_re, value_re)

    def compare_ids(self, metadata1: DataFrameMetadata, metadata2: DataFrameMetadata) -> pd.DataFrame:
        """
        Compare all id columns. Compare if they contain nulls.
        Compare embeddings of values.
        Compare ratio of max length.
        Make an average of these values.
        :return: matrix containing float numbers in range <0, 1>
        """
        nulls_re = pd.DataFrame()
        value_long_re = pd.DataFrame()
        value_short_re = pd.DataFrame()
        ratio_max_re = pd.DataFrame()
        are_nulls = self.__are_columns_null(metadata1.column_kind[DataKind.ID], metadata2.column_kind[DataKind.ID],
                                            "ID metadata")
        if are_nulls[0]:
            return are_nulls[1]
        for column1 in metadata1.column_kind[DataKind.ID]:
            for column2 in metadata2.column_kind[DataKind.ID]:
                for value_re, attribute in [(value_long_re, 'longest'), (value_short_re, 'shortest')]:
                    embeddings1 = getattr(metadata1.kind_metadata[column1], f'{attribute}_embeddings')
                    embeddings2 = getattr(metadata2.kind_metadata[column2], f'{attribute}_embeddings')
                    attribute1 = getattr(metadata1.kind_metadata[column1], attribute)
                    attribute2 = getattr(metadata2.kind_metadata[column2], attribute)

                    if embeddings1 is None or embeddings2 is None:
                        value_re.loc[column1, column2] = 0 if attribute1 == attribute2 else 1
                    else:
                        value_re.loc[column1, column2] = 1 - cosine_sim(embeddings1, embeddings2)
                nulls_re.loc[column1, column2] = 0 if metadata1.kind_metadata[column1].nulls == metadata2.kind_metadata[
                    column2].nulls else 1
                ratio_max_re.loc[column1, column2] = abs(
                    metadata1.kind_metadata[column1].ratio_max_length - metadata2.kind_metadata[
                        column2].ratio_max_length)

        return self.concat(value_short_re, value_long_re, ratio_max_re, nulls_re)

    def compare_bools(self, metadata1: DataFrameMetadata, metadata2: DataFrameMetadata) -> pd.DataFrame:
        """
        Compare all boolean columns. Compare if they have the same distribution of True and False values.
        Compare if they contain nulls.
        Compare embeddings of values.
        Make an average of these values.
        :param metadata1: for column1
        :param metadata2: for column2
        :return: matrix containing float numbers in range <0, 1>
        """
        value_re = pd.DataFrame()
        distr_re = pd.DataFrame()
        nulls_re = pd.DataFrame()
        are_nulls = self.__are_columns_null(metadata1.column_kind[DataKind.BOOL],
                                            metadata2.column_kind[DataKind.BOOL],
                                            "Boolean metadata")
        if are_nulls[0]:
            return are_nulls[1]
        for column1 in metadata1.column_kind[DataKind.BOOL]:
            for column2 in metadata2.column_kind[DataKind.BOOL]:
                nulls_re.loc[column1, column2] = 0 if metadata1.kind_metadata[column1].nulls == metadata2.kind_metadata[
                    column2].nulls else 1
                distr_re.loc[column1, column2] = abs(
                    metadata1.kind_metadata[column1].distribution[0] / metadata1.kind_metadata[column1].distribution[1]
                    -
                    metadata2.kind_metadata[column2].distribution[0] / metadata2.kind_metadata[column2].distribution[1])
                if (metadata1.kind_metadata[column1].value_embeddings is None or
                        metadata2.kind_metadata[column2].value_embeddings is None):
                    value_re.loc[column1, column2] = 0
                else:
                    value_re.loc[column1, column2] = self.compute_embeddings_distance(
                        metadata1.kind_metadata[column1].value_embeddings,
                        metadata2.kind_metadata[column2].value_embeddings)
        return self.concat(value_re, distr_re, nulls_re)

    def compare_categorical(self, metadata1: DataFrameMetadata, metadata2: DataFrameMetadata) -> pd.DataFrame:
        """
        Compare all categorical columns. Compare if they contain nulls.
        Compare embeddings of values.
        Make an average of these values.
        :param metadata1: for column1
        :param metadata2: for column2
        :return: matrix containing float numbers in range <0, 1>
        """
        value_re = pd.DataFrame()
        count_re = pd.DataFrame()
        are_nulls = self.__are_columns_null(metadata1.column_kind[DataKind.CATEGORICAL],
                                            metadata2.column_kind[DataKind.CATEGORICAL],
                                            "Categorical metadata")
        if are_nulls[0]:
            return are_nulls[1]
        for column1 in metadata1.column_kind[DataKind.CATEGORICAL]:
            for column2 in metadata2.column_kind[DataKind.CATEGORICAL]:
                value_re.loc[column1, column2] = self.compute_embeddings_distance(
                    metadata1.categorical_metadata[column1].category_embedding,
                    metadata2.categorical_metadata[column2].category_embedding)
                count1 = metadata1.categorical_metadata[column1].count_categories
                count2 = metadata2.categorical_metadata[column2].count_categories
                count_re.loc[column1, column2] = count1 / count2 if count1 < count2 else count2 / count1
                # todo compare categories_with_count for metadata1 and metadata2
                # firstly normalize dictionary categories_with_count then
                # compare the difference between the two dictionaries
        return self.concat(value_re, count_re)

    def compare(self, metadata1: DataFrameMetadata, metadata2: DataFrameMetadata, distance_function: DistanceFunction,
                settings: set[Settings]) -> pd.DataFrame:
        """
        Compare kind columns
        :param distance_function: - to use for computing distance
        :param metadata1: first table
        :param metadata2: second table
        :param settings: - for another kind information
        :return: dataframe full of numbers between 0 and 1
        """
        result = 0
        if DataKind.BOOL in self.compare_kind:
            bools = self.compare_bools(metadata1, metadata2)
            result += self.compute_result(bools, distance_function, settings, self.kind_weight[DataKind.BOOL])
        if DataKind.CONSTANT in self.compare_kind:
            constants = self.compare_constants(metadata1, metadata2)
            result += self.compute_result(constants, distance_function, settings, self.kind_weight[DataKind.CONSTANT])
        if DataKind.ID in self.compare_kind:
            ids = self.compare_ids(metadata1, metadata2)
            result += self.compute_result(ids, distance_function, settings, self.kind_weight[DataKind.ID])
        if DataKind.CATEGORICAL in self.compare_kind:
            categorical = self.compare_categorical(metadata1, metadata2)
            result += self.compute_result(categorical, distance_function, settings,
                                          self.kind_weight[DataKind.CATEGORICAL])
        return pd.DataFrame([result])


class Comparator:
    """
    Comparator for comparing two tables
    """

    def __init__(self):
        self.comparator_type: list[ComparatorType] = []
        self.settings: set[Settings] = set()
        self.distance_function = HausdorffDistanceMin()

    def set_distance_function(self, distance_function: DistanceFunction) -> 'Comparator':
        """
        Set distance function for comparing two tables
        """
        self.distance_function = distance_function
        return self

    def set_settings(self, settings: set) -> 'Comparator':
        """
        Set settings for comparing two tables
        """
        self.settings = settings
        return self

    def add_settings(self, setting: Settings) -> 'Comparator':
        """
        Add setting for comparing two tables
        """
        self.settings.add(setting)
        return self

    def add_comparator_type(self, comparator: ComparatorType) -> 'Comparator':
        """
         Add comparator
        """
        self.comparator_type.append(comparator)
        return self

    def compare(self, metadata1: DataFrameMetadata, metadata2: DataFrameMetadata):
        """
        Compare two tables according to previously set properties.
        """
        distances = []
        for comp in self.comparator_type:
            distance_table = comp.compare(metadata1, metadata2, self.distance_function, self.settings)
            distances.append((self.distance_function.compute(distance_table),
                              get_ratio(distance_table.shape[0], distance_table.shape[1]),
                              comp.weight
                              ))
        result = 0
        nan = 0
        for dist, ratio, weight in distances:
            if math.isnan(dist):
                nan += 1
                continue
            if Settings.NO_RATIO in self.settings:
                result += dist * dist * weight
            else:
                result += dist * dist * ratio * weight
        if nan == len(distances):
            return 1
        return np.sqrt(result)
