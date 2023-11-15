from pprint import pprint

import numpy as np
import pandas as pd

from DataFrameMetadata import DataFrameMetadata
from functions import DataFrameWithStat


class SimilarityData:
    def __init__(self):
        self._score = 1

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, new_score):
        if new_score < 0:
            raise ValueError("new score cant be below 0")
        self._score = new_score


def most_frequent(list: list[(float, str)]) -> str:
    """
    Gets names from list (second argument) then it returns most common name
    :param list: of values and names
    :return: most common name
    """
    names = []
    for i in list:
        names.append(i[1])

    return max(set(names), key=names.count)


class ComparatorForDatasets:
    # {name: DataFrameWithStat(table) for table, name in zip(database, names)}
    def __init__(self, database: dict[str, DataFrameMetadata]):
        self.database = database
        self.similarity = dict
        self.threshold = 0.7  # todo

    def cosine(self, u, v):
        return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

    def cross_compare(self):
        for table_name, table in self.database.items():
            similarity_values_for_columns = []
            for column_emb in table.column_embeddings.values():
                all_res = []
                for name, to_compare in self.database.items():
                    if table is to_compare:
                        continue
                    for to_comp_emb in to_compare.column_embeddings.values():
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