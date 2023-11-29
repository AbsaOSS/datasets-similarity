import logging
import struct

import numpy as np
import pandas as pd

from DataFrameMetadata import DataFrameMetadata
from collections import defaultdict
from itertools import compress

class CategoricalSimilarity:

    def __init__(self):
        self.categories_ratio: float
        self.most_common: tuple[str, str]
        self.least_common: tuple[str, str]
        self.number_of_similar_categories: int
        self.similarity: list


class SimilarityStruct:
    def __init__(self, table_name: str, column_name: str, similarity: float):
        self.table_name = table_name
        self.column_name = column_name
        self.similarity = similarity
        self.categorical_similarity = CategoricalSimilarity

    def add_categorical_similarity_struct(self, categorical: CategoricalSimilarity):
        self.categorical_similarity = categorical

    def __lt__(self, other):
        return self.similarity < other.similarity

    def __le__(self, other):
        return self.similarity <= other.similarity

    def __eq__(self, other):
        return self.similarity == other.similarity

    def __ne__(self, other):
        return self.similarity != other.similarity

    def __gt__(self, other):
        return self.similarity > other.similarity

    def __ge__(self, other):
        return self.similarity >= other.similarity


class SimilarityData:

    def __init__(self):
        self._score = 1
        self.similarity_columns: dict[str, list[SimilarityStruct]] = defaultdict(list)

    def add_to_similarity_columns(self, key: str, value: list[SimilarityStruct]):
        self.similarity_columns[key] = value

    def get_similar_columns(self, colum_name: str) -> list[SimilarityStruct]:
        """

        :param colum_name: column for which we want similar columns
        :return: list of similar columns
        """
        return self.similarity_columns[colum_name]

    def count_most_similar(self):
        dummy_table_sim = []
        for i in self.similarity_columns.values():
            if i:
                dummy_table_sim.append((max(i).similarity, max(i).table_name))
        most = most_frequent(dummy_table_sim)

        # count = 0
        # avg = 0
        # for i in dummy_table_sim:
        #     if i[1] == most:
        #         avg += i[0]
        #         count += 1

        # print(table_name, " is most similar to ", most, " by ", avg / count)
        return most


def most_frequent(list: list[(float, str)]) -> str:
    """
    Gets names from list (second argument) then it returns most common name
    :param list: of values and names
    :return: most common name
    """
    names = []
    for i in list:
        names.append(i[1])

    return max(set(names), key=names.count) # todo change if two names are pressent same nuber of times


class ComparatorForDatasets:
    # {name: DataFrameWithStat(table) for table, name in zip(database, names)}
    def __init__(self, database: dict[str, DataFrameMetadata]):
        self.database = database
        self.similarity: dict[str, SimilarityData] = defaultdict()
        self.threshold = 0.7  # todo

    def cosine(self, u, v):
        return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

    def cross_compare(self) -> dict:
        result = {}
        for table_name, table in self.database.items():
            similarity_data = SimilarityData()
            for column_name, column_emb in table.column_embeddings.items():
                sim_columns = []
                for name, to_compare in self.database.items():
                    if table is to_compare:
                        continue
                    for to_comp_colum_name, to_comp_emb in to_compare.column_embeddings.items():
                        sim = self.cosine(column_emb, to_comp_emb)
                        if sim > self.threshold:
                            sim_columns.append(SimilarityStruct(name, to_comp_colum_name, sim))
                similarity_data.add_to_similarity_columns(key=column_name, value=sim_columns)
            self.similarity[table_name] = similarity_data
            result[table_name] = self.similarity[table_name].count_most_similar()
        return result

    def compare_categorical(self):
        for table_name, table in self.database.items():
            column_names = list(compress(table.column_names, table.column_categorical))
            for name, to_compare in self.database.items():
                if table is not to_compare:
                    column_names_to_comp = list(compress(to_compare.column_names, to_compare.column_categorical))
                    for c_name in column_names:
                        for c_name_compare in column_names_to_comp:
                            table[c_name]
                            to_compare[c_name_compare]


    def cross_compare_column_names(self):
        result = {}
        for table_name, table in self.database.items():
            if table_name == "disney_movies":
                logging.debug("")
            similarity_values_for_columns = []
            for column_emb in table.column_name_embeddings:
                all_res = []
                for name, to_compare in self.database.items():
                    if table is to_compare:
                        continue
                    for to_comp_emb in to_compare.column_name_embeddings:
                        sim = self.cosine(column_emb, to_comp_emb)
                        all_res.append((sim, name))  # todo save also column name ?
                similarity_values_for_columns.append(max(all_res))  # simillarity for each column to some another column
            ## todo remove
            most = most_frequent(similarity_values_for_columns)
            count = 0
            avg = 0
            for i in similarity_values_for_columns:
                if i[1] == most:
                    avg += i[0]
                    count += 1

            print(table_name, " is most similar to ", most, " by ", avg / count)
            result[table_name] = most
        return result
