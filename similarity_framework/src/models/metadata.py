"""
File contains Table metadata (DataFrameMetadata class) and other metadata classes (CategoricalMetadata, KindMetadata ...)
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Optional, Any, List

import pandas as pd
from pandas import Series
from torch import Tensor

from similarity_framework.src.models.types_ import (
    DataKind,
    Type,
    COMPUTER_GENERATED,
    HUMAN_GENERATED,
    INT,
    FLOAT,
    NUMERICAL,
    NONNUMERICAL,
    WORD,
    ALPHABETIC,
    ALPHANUMERIC,
    ALL,
    SENTENCE,
    ARTICLE,
    PHRASE,
    MULTIPLE_VALUES,
)


class CategoricalMetadata:
    """
    Metadata for categorical columns
    only text based columns
    count_categories: number of categories
    categories: set of categories
    categories_with_count: dict of categories with count
    category_embedding: embedding for each category
    """

    def __init__(self, count: int, categories: list, categories_with_count: Series, category_embedding: list[Tensor]):
        self.count_categories = count
        self.categories = set(categories)
        self.categories_with_count = categories_with_count
        self.category_embedding = category_embedding
        # self.categories_embeddings = categories_embeddings


class KindMetadata:
    pass


class BoolMetadata(KindMetadata):
    """
    Metadata for boolean columns
    """

    def __init__(
        self,
        value: tuple,
        distribution: tuple[int, ...],
        null_values: Optional[bool],
        model,
    ):
        self.distribution = distribution
        self.nulls = null_values
        self.value = value
        self.value_embeddings = None if type(value[0]) is not str else model.encode(list(value))

    def __str__(self):
        return f"BoolMetadata(values={self.value},distribution={self.distribution}, null_values={self.nulls})"


class IDMetadata(KindMetadata):
    """
    Metadata for ID columns
    """

    def __init__(
        self,
        longest: Any,
        shortest: Any,
        null_values: Optional[bool],
        ratio_max_length: float,
        model,
    ):
        self.nulls = null_values
        self.longest = longest
        self.shortest = shortest
        self.longest_embeddings = None if type(longest) is not str else model.encode(longest)
        self.shortest_embeddings = None if type(shortest) is not str else model.encode(shortest)
        self.ratio_max_length = ratio_max_length

    def __str__(self):
        return f"IDMetadata(null_values={self.nulls}," f" longest={self.longest}, shortest={self.shortest}, ratio_max_length={self.ratio_max_length})"


class ConstantMetadata(KindMetadata):
    """
    Metadata for constant columns
    """

    def __init__(
        self,
        value: tuple,
        distribution: Optional[tuple[int, ...]],
        null_values: Optional[bool],
        model,
    ):
        self.nulls = null_values
        self.value = value
        self.distribution = distribution
        self.value_embeddings = None if type(value[0]) is not str else model.encode(list(value))

    def __str__(self):
        return f"ConstantMetadata(values={self.value}, null_values={self.nulls}, distribution={self.distribution})"


class NonnumericalMetadata:
    """
    Metadata for nonnumerical columns

    It is store longest and shortest str, average length

    It should also store bigrams, trigrams ...
    """

    def __init__(
        self,
        longest: str,
        shortest: str,
        avg_length: int,
    ):
        self.longest = longest
        self.shortest = shortest
        self.avg_length = avg_length

    def __str__(self):
        return f"NonnumericalMetadata(longest={self.longest}, shortest={self.shortest}, avg_length={self.avg_length})"


class NumericalMetadata:
    """
    Metadata for numerical columns

    It is store range, range size, if values have the same length

    It should also store distribution
    """

    def __init__(
        self,
        min_value: float | int,
        max_value: float | int,
        same_value_length: bool,
    ):
        self.min_value = min_value
        self.max_value = max_value
        self.range_size = max_value - min_value
        self.same_value_length = same_value_length
        # todo distribution !!!!!!

    def __str__(self):
        return (
            f"NumericalMetadata(min_value={self.min_value}, max_value={self.max_value},"
            f" range_size={self.range_size}, same_value_length={self.same_value_length})"
        )


class Metadata:
    """
    Metadata for Table
    """

    def __init__(self, name: str = "unknown"):
        # default
        self.name = name
        self.size = int
        self.column_names: list[str] = []
        self.column_names_clean: dict[str, str] = defaultdict()
        self.column_incomplete: dict[str, bool] = defaultdict()

        # compute_*_type
        self.column_type: dict[type[Type], set[str]] = defaultdict(set)
        self.numerical_metadata: dict[str, NumericalMetadata] = defaultdict()
        self.nonnumerical_metadata: dict[str, NonnumericalMetadata] = defaultdict()

        # compute_column_kind
        self.column_kind: dict[DataKind, set[str]] = defaultdict(set)
        self.kind_metadata: dict[str, KindMetadata] = defaultdict()
        self.categorical_metadata: dict[str, CategoricalMetadata] = defaultdict()

        # compute_column_names_embeddings
        self.column_name_embeddings = {}

        # create_column_embeddings
        self.column_embeddings = {}

        # compute correlated columns
        self.correlated_columns = set()  # todo

    def get_column_names_by_kind(self, *kinds: DataKind) -> List[str]:
        """
        Get column names by kind
        """
        columns: list = []
        for t in kinds:
            columns.extend(self.column_kind[t])
        return columns

    def get_column_names_by_type(self, *types: type[Type]) -> List[str]:
        """
        Get column names by type
        """
        if NONNUMERICAL in types:
            types = list(types)  # todo check if the list is necessary
            types.extend([WORD, ALPHABETIC, ALPHANUMERIC, ALL, SENTENCE, ARTICLE, PHRASE, MULTIPLE_VALUES])
        columns: list = []
        for t in types:
            columns.extend(self.column_type[t])
        return columns

    def get_numerical_columns_names(self):
        """
        Get column names for numerical column
        """
        return self.get_column_names_by_type(NUMERICAL, FLOAT, INT, HUMAN_GENERATED, COMPUTER_GENERATED)

    def get_column_type(self, name: str) -> type[Type] | None:
        """
        Get column type by column name
        """
        for column_type, columns in self.column_type.items():
            if name in columns:
                return column_type
        return None

    def get_column_kind(self, name: str) -> DataKind | None:
        """
        Get column kind by column name
        """
        for column_kind, columns in self.column_kind.items():
            if name in columns:
                return column_kind
        return None


@dataclass
class MetadataCreatorInput:
    dataframe: pd.DataFrame
    source_name: str = "unknown"
