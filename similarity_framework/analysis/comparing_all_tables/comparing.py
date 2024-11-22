"""Comparator for comparing all tables together"""

import dataclasses
from typing import Optional
from itertools import compress
from collections import defaultdict

import numpy as np

from similarity_framework.src.models.metadata import Metadata

@dataclasses.dataclass
class CategoricalSimilarity:
    """
    Struct for categorical similarity
    """

    categories_ratio: float
    count_similar: Optional[int] = None
    similarity_score: Optional[int] = None


@dataclasses.dataclass
class SimilarityStruct:
    """
    Similarity struct for one column comparing with another column
    """

    table_name: Optional[str] = None
    column_name: Optional[str] = None
    similarity: Optional[float] = None
    categorical_similarity: Optional[CategoricalSimilarity] = None

    def __lt__(self, other: "SimilarityStruct") -> bool:
        return self.similarity < other.similarity

    def __le__(self, other: "SimilarityStruct") -> bool:
        return self.similarity <= other.similarity

    def __eq__(self, other: "SimilarityStruct") -> bool:
        return self.similarity == other.similarity

    def __ne__(self, other: "SimilarityStruct") -> bool:
        return self.similarity != other.similarity

    def __gt__(self, other: "SimilarityStruct") -> bool:
        return self.similarity > other.similarity

    def __ge__(self, other: "SimilarityStruct") -> bool:
        return self.similarity >= other.similarity


class SimilarityData:
    """
    Similarity data for one table
    """

    def __init__(self):
        """
        similarity_columns, str represents name of column, list similarity to all other columns
        """
        self._score = 1
        self.similarity_columns: dict[str, list[SimilarityStruct]] = defaultdict(list)

    def add_to_similarity_columns(self, key: str, value: list[SimilarityStruct]):
        """
        Adds similarity to columns
        """
        self.similarity_columns[key] = value

    def get_similar_columns(self, colum_name: str) -> list[SimilarityStruct]:
        """

        :param colum_name: column for which we want similar columns
        :return: list of similar columns
        """
        return self.similarity_columns[colum_name]

    def count_most_similar(self):
        """
        Method counts most similar table for each column
        """
        dummy_table_sim = []
        for i in self.similarity_columns.values():
            if i:
                dummy_table_sim.append(
                    (
                        max(i).similarity,
                        max(i).table_name,
                    )
                )
        most = most_frequent(dummy_table_sim)

        # count = 0
        # avg = 0
        # for i in dummy_table_sim:
        #     if i[1] == most:
        #         avg += i[0]
        #         count += 1

        # print(table_name, " is most similar to ", most, " by ", avg / count)
        return most


def most_frequent(list_: list[(float, str)]) -> str:
    """
    Gets names from list (second argument) then it returns most common name
    :param list_: of values and names
    :return: most common name
    """
    names = []
    for i in list_:
        names.append(i[1])

    return max(set(names), key=names.count)  # todo change if two names are pressent same nuber of times


class ComparatorForDatasets:
    """
    This class gets dictionary of datasets metadata to compare
    """

    # {name: DataFrameWithStat(table) for table, name in zip(database, names)}
    def __init__(
        self,
        database: dict[str, Metadata],
    ):
        self.database = database
        self.similarity: dict[str, SimilarityData] = defaultdict()
        self.threshold = 0.7  # todo

    def cosine(self, u: list, v: list) -> float:
        """
        Computes cosine similarity
        """
        return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

    def cross_compare(self) -> dict:
        """
        Methods counts similarity of columns for which we have embeddings
        :return:
        """
        result = {}
        for (
            table_name,
            table,
        ) in self.database.items():
            similarity_data = SimilarityData()
            for (
                column_name,
                column_emb,
            ) in table.column_embeddings.items():
                sim_columns = []
                for (
                    name,
                    to_compare,
                ) in self.database.items():
                    if table is to_compare:
                        continue
                    for (
                        to_comp_colum_name,
                        to_comp_emb,
                    ) in to_compare.column_embeddings.items():
                        sim = self.cosine(
                            column_emb,
                            to_comp_emb,
                        )
                        if sim > self.threshold:
                            sim_columns.append(
                                SimilarityStruct(
                                    name,
                                    to_comp_colum_name,
                                    sim,
                                )
                            )
                similarity_data.add_to_similarity_columns(
                    key=column_name,
                    value=sim_columns,
                )
            self.similarity[table_name] = similarity_data
            result[table_name] = self.similarity[table_name].count_most_similar()
        return result

    def compare_categorical(self):
        """
        Method compares categorical columns
        """
        for _, table in self.database.items():
            column_names = list(compress(table.column_names, table.column_categorical))
            for _, to_compare in self.database.items():
                if table is not to_compare:
                    column_names_to_comp = list(
                        compress(
                            to_compare.column_names,
                            to_compare.column_categorical,
                        )
                    )
                    for c_name in column_names:
                        for c_name_compare in column_names_to_comp:
                            table[c_name]
                            to_compare[c_name_compare]

    def cross_compare_column_names(self) -> dict:
        """
        Method counts similarity for all tables by using column names
        :return:
        """
        result = {}
        for (
            table_name,
            table,
        ) in self.database.items():
            similarity_values_for_columns = []
            for column_emb in table.column_name_embeddings.values():
                all_res = []
                for (
                    name,
                    to_compare,
                ) in self.database.items():
                    if table is to_compare:
                        continue
                    for to_comp_emb in to_compare.column_name_embeddings.values():
                        sim = self.cosine(
                            column_emb,
                            to_comp_emb,
                        )
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

            print(
                table_name,
                " is most similar to ",
                most,
                " by ",
                avg / count,
            )
            result[table_name] = most
        return result
