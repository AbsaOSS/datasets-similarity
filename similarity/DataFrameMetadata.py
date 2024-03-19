from collections import defaultdict
from typing import Generator, Optional, Any
from similarity.Types import DataKind, Type, COMPUTER_GENERATED, HUMAN_GENERATED, INT, FLOAT, NUMERICAL, NONNUMERICAL, \
    WORD, ALPHABETIC, ALPHANUMERIC, ALL, SENTENCE, ARTICLE, PHRASE, MULTIPLE_VALUES


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
    ratio_max_length = for ID (max value)/(size column)

    todo format (uuid, rodc, visa/mastercard ...)
    """

    def __init__(self, value: Optional[tuple], distribution: Optional[tuple[int, ...]],
                 longest: Optional[Any], shortest: Optional[Any], null_values: Optional[bool],
                 ratio_max_length: Optional[float], model):
        self.kind_metadata = None
        self.value = value
        self.value_embeddings = None if value is None or value[0] is not str else model.encode(list(value))
        self.distribution = distribution
        self.longest = longest
        self.shortest = shortest
        self.longest_embeddings = None if value is None or value[0] is not str else model.encode(longest)
        self.shortest_embeddings = None if value is None or value[0] is not str else model.encode(shortest)
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

    def __init__(self, min_value: float | int, max_value: float | int, same_value_length: bool):
        self.min_value = min_value
        self.max_value = max_value
        self.range_size = max_value - min_value
        self.same_value_length = same_value_length
        # todo distribution !!!!!!


class DataFrameMetadata:
    def __init__(self):
        # default
        self.size = int
        self.column_names: list[str] = list()
        self.column_names_clean: dict[str, str] = defaultdict()
        self.column_incomplete: dict[str, bool] = defaultdict()
        self.correlated_columns = set()  # todo

        # compute_*_type
        self.type_column: dict[Type, set[str]] = defaultdict(set)
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

    def get_column_type(self, name):
        for column_type, columns in self.type_column.items():
            if name in columns:
                return column_type

    def get_column_names_by_type(self, *types):
        if NONNUMERICAL in types:
            types = list(types)
            types.extend([WORD, ALPHABETIC, ALPHANUMERIC, ALL, SENTENCE, ARTICLE, PHRASE, MULTIPLE_VALUES])
        columns = []
        for t in types:
            columns.extend(self.type_column[t])
        return columns

    def get_numerical_columns_names(self):
        return self.get_column_names_by_type(NUMERICAL, FLOAT,
                                             INT,
                                             HUMAN_GENERATED,
                                             COMPUTER_GENERATED)
