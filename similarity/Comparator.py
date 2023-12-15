from abc import abstractmethod, ABC

import numpy as np
import pandas as pd

from similarity.DataFrameMetadata import DataFrameMetadata


def cosine(u, v):  ## todo move to functions.py?
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))


def get_ratio(count1: int, count2: int):
    if count1 == 0 or count2 == 0:
        return 1
    if count1 < count2:
        return count2 / count1
    else:
        return count1 / count2


class DistanceFunction(ABC):
    @abstractmethod
    def compute(self, distance_table: pd.DataFrame):
        pass


class HausdorffDistanceMin(DistanceFunction):
    def compute(self, distance_table: pd.DataFrame):
        if distance_table.size == 0:
            return np.nan
        row_mins = []
        column_mins = []
        for index, row in distance_table.iterrows():
            row_mins.append(min(row))
        for _, column in distance_table.items():
            column_mins.append(min(column))
        return min([max(row_mins), max(column_mins)])


class ComparatorType(ABC):
    @abstractmethod
    def compare(self, metadata1: DataFrameMetadata, metadata2: DataFrameMetadata) -> pd.DataFrame:
        pass

    def concat(self, *data_frames) -> pd.DataFrame:
        """
        Concat all dataframes together, compute avg for each cell
        :param data_frames: array of dataframes
        :return: new dataframe
        """
        res = data_frames[0]
        for d in data_frames[1:]:
            res.add(d).map(lambda x: x / len(data_frames))
        return res


class CategoricalComparator(ComparatorType):

    def __compute_distance(self, dist_matrix): # Hausdorff
        row_mins = []
        column_mins = []
        for row in dist_matrix:
            row_mins.append(min(row))
        for column in zip(*dist_matrix):
            column_mins.append(min(column))
        return min([max(row_mins), max(column_mins)])

    def __create_dist_matrix(self, embeddings1, embeddings2):
        simil_matrix = []
        for embed1 in embeddings1:
            siml_line = []
            for embed2 in embeddings2:
                # todo rounding for 3 digits ? ok -> two because of minus 0
                siml_line.append(round(1 - round(cosine(embed1, embed2), 4), 3)) # distance is 1- similarity
            simil_matrix.append(siml_line)
        return simil_matrix


    def compare(self, metadata1: DataFrameMetadata, metadata2: DataFrameMetadata) -> pd.DataFrame:
        result = pd.DataFrame()
        name_distance = pd.DataFrame()
        for id1, (column1, categorical1) in enumerate(metadata1.categorical_metadata.items()):
            for id2, (column2, categorical2) in enumerate(metadata2.categorical_metadata.items()):
                simil_matrix = self.__create_dist_matrix(categorical1.category_embedding,
                                                         categorical2.category_embedding)
                # count, score = self.__compute_similarity_score(simil_matrix)
                dist = self.__compute_distance(simil_matrix)
                ratio = get_ratio(categorical1.count_categories, categorical1.count_categories)# todo 1-ratio???
                # result.loc[id1, id2] = 1 - (score * ratio)  # todo
                result.loc[id1, id2] = dist * ratio  # todo
                name_distance.loc[id1, id2] = 1 - cosine(metadata1.column_name_embeddings[column1],
                                                 metadata2.column_name_embeddings[column2])
        ## todo p value or correlation
        return self.concat(result, name_distance)

class CategoricalComparatorSimilar(CategoricalComparator):
    def __create_sim_matrix(self, embeddings1, embeddings2):
        simil_matrix = []
        for embed1 in embeddings1:
            siml_line = []
            for embed2 in embeddings2:
                siml_line.append( round(cosine(embed1, embed2), 3))
            simil_matrix.append(siml_line)
        return simil_matrix

    def __compute_similarity_score(self, similarity_matrix):  ## todo test some other methods
        # todo use Haufsdorfe distance ?
        res = 0
        count = 0
        trashold = 0.7 # todo set from outside
        length = 0
        for i in similarity_matrix:
            avg = sum(i) / len(i)
            length = len(i)
            if max(i) > trashold:
                count += 1
            res += max(i)
        return count, res / len(similarity_matrix) * (count / len(similarity_matrix))

    def compare(self, metadata1: DataFrameMetadata, metadata2: DataFrameMetadata) -> pd.DataFrame:
        result = pd.DataFrame()
        name_distance = pd.DataFrame()
        for id1, (column1, categorical1) in enumerate(metadata1.categorical_metadata.items()):
            for id2, (column2, categorical2) in enumerate(metadata2.categorical_metadata.items()):
                simil_matrix = self.__create_sim_matrix(categorical1.category_embedding,
                                                         categorical2.category_embedding)
                count, score = self.__compute_similarity_score(simil_matrix)
                ratio = get_ratio(categorical1.count_categories, categorical1.count_categories)  # todo 1-ratio???
                result.loc[id1, id2] = 1 - (score * ratio)
                name_distance.loc[id1, id2] = 1 - cosine(metadata1.column_name_embeddings[column1],
                                                         metadata2.column_name_embeddings[column2])
        ## todo p value or correlation
        return self.concat(result, name_distance)


class ColumnEmbeddingComparator(ComparatorType):
    def compare(self, metadata1: DataFrameMetadata, metadata2: DataFrameMetadata) -> pd.DataFrame:
        ## todo originally it was used threshold here
        result = pd.DataFrame()
        name_distance = pd.DataFrame()
        for id1, (column1, embedding1) in enumerate(metadata1.column_embeddings.items()):
            for id2, (column2, embedding2) in enumerate(metadata2.column_embeddings.items()):
                result.loc[id1,id2] = 1 - cosine(embedding1, embedding2)
                name_distance.loc[id1,id2] = 1 - cosine(metadata1.column_name_embeddings[column1],
                                                 metadata2.column_name_embeddings[column2])
        return self.concat(result, name_distance)


class Comparator:
    def __init__(self):
        self.comparator_type: list[ComparatorType] = []
        self.settings = []
        self.distance_function = HausdorffDistanceMin()

    def set_distance_function(self, distance_function: DistanceFunction) -> 'Comparator':
        self.distance_function = distance_function
        return self

    def set_settings(self, settings: list) -> 'Comparator':
        self.settings = settings
        return self

    def add_settings(self, setting) -> 'Comparator':
        self.settings.append(setting)
        return self

    def add_comparator_type(self, comparator: ComparatorType) -> 'Comparator':
        self.comparator_type.append(comparator)
        return self

    def compare(self, metadata1: DataFrameMetadata, metadata2: DataFrameMetadata):
        distances = []
        for comp in self.comparator_type:
            distance_table = comp.compare(metadata1, metadata2)
            distances.append((self.distance_function.compute(distance_table),
                              get_ratio(distance_table.shape[0], distance_table.shape[1])
                              ))
        result = 0
        for dist, weight in distances:
            result += dist * dist * weight
        return np.sqrt(result)
