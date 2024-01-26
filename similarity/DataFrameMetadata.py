import hashlib
import pickle
from collections import defaultdict, Counter
from typing import Generator, Optional, Any
from similarity.Types import Types, DataKind


def dumps(value):
    if isinstance(value, Generator):
        value = [val for val in value]
    return value


class CategoricalMetadata:
    """
    Metadata for categorical columns
    todo

    """

    def __init__(self, count: int, categories: list, categories_with_count, category_embedding):
        self.count_categories = count
        self.categories = set(categories)
        self.categories_with_count = categories_with_count
        self.category_embedding = category_embedding
        # self.categories_embeddings = categories_embeddings


class KindMetadata:
    """
    Metadata for kind
    value: for BOOL tuple and CONSTANT one value
    distribution: for BOOL
    longest: for ID
    shortest: for ID
    nulls: for BOOL, CONSTANT, ID
    ratio_max_length = for CONSTANT (max value)/(size column)

    todo format (uuid, rodc, visa/mastercard ...)
    """

    def __init__(self, value: Optional[tuple], distribution: Optional[tuple[int, ...]],
                 longest: Optional[Any], shortest: Optional[Any], null_values: Optional[bool],
                 ratio_max_length: Optional[float]):
        self.value = value
        self.distribution = distribution
        self.longest = longest
        self.shortest = shortest
        self.nulls = null_values
        self.ratio_max_length = ratio_max_length


class NonnumericalMetadata:
    """
    Metadata for nonnumerical columns

    It is store longest and shortest str, average length

    It should also store bigrams, trigrams ...
    """
    def __init__(self, longest: str, shortest: str, avg_length: int):
        self.longest = longest
        self.shortest = shortest
        self.avg_length = avg_length
        # todo bigrams trigrams ?
        # todo embeddings ?? nebo mame pro cele sloupce ?


class NumericalMetadata:
    """
    Metadata for numerical columns

    It is store range, range size, if values have the same length

    It should also store distribution
    """
    def __init__(self, min_value: float | int,  max_value: float | int, same_value_length: bool):
        self.min_value = min_value
        self.max_value = max_value
        self.range_size = max_value - min_value
        self.same_value_length = same_value_length
        # todo distribution !!!!!!


class DataFrameMetadata:
    def __init__(self):
        self.size = int
        self.column_names = list()
        self.column_names_clean = list()
        self.column_name_embeddings = {}
        self.type_column: dict[Types, set[str]] = defaultdict(set)
        self.column_kind: dict[DataKind, set[str]] = defaultdict(set)
        self.column_incomplete = list()
        self.column_embeddings = {}
        self.correlated_columns = set()
        self.categorical_metadata: dict[str, CategoricalMetadata] = defaultdict()
        self.kind_metadata: dict[str, KindMetadata] = defaultdict()
        self.numerical_metadata: dict[str, NumericalMetadata] = defaultdict()
        self.nonnumerical_metadata: dict[str, NonnumericalMetadata] = defaultdict()

    def get_column_type(self, name):
        for column_type, columns in self.type_column.items():
            if name in columns:
                return column_type

    def get_column_names_by_type(self, *types):
        columns = []
        for t in types:
            columns.extend(self.type_column[t])
        return columns

    def get_numerical_columns_names(self):
        return self.get_column_names_by_type(Types.NUMERICAL, Types.NUMERICAL.value.FLOAT,
                                             Types.NUMERICAL.value.INT,
                                             Types.NUMERICAL.value.FLOAT.value.HUMAN_GENERATED,
                                             Types.NUMERICAL.value.FLOAT.value.COMPUTER_GENERATED)
