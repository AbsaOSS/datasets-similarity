import hashlib
import pickle
from collections import defaultdict, Counter
from typing import Generator

from Types import Types

def dumps(value):
    if isinstance(value, Generator):
        value = [val for val in value]
    return value

class CategoricalMetadata:
    # def __init__(self):
    #     self.count_categories = int
    #     self.categories = list(str)
    #     self.categories_with_count = list()

    def __init__(self, count, categories, categories_with_count):
        self.count_categories = count
        self.categories = set(categories)
        self.categories_with_count = categories_with_count
        # self.categories_embeddings = categories_embeddings

    def hash(self) -> bytes:
        return (pickle.dumps(self.count_categories) +
                pickle.dumps(self.categories) +
                pickle.dumps(self.categories_with_count))

class DataFrameMetadata:
    def __init__(self):
        self.size = int
        self.column_names = list()
        self.column_names_clean = list()
        self.column_name_embeddings = list()
        self.type_column: dict[Types, set[str]] = defaultdict(set)
        self.column_categorical = list()
        self.column_incomplete = list()
        self.column_embeddings = {}
        self.correlated_columns = set()
        self.categorical_metadata: dict[str, CategoricalMetadata] = defaultdict()

    def hash(self) -> bytes:
        m = hashlib.sha256()
        m.update(bytes(self.size))
        m.update(bytes(''.join(self.column_names), 'utf-8'))
        m.update(bytes(''.join(self.column_names_clean), 'utf-8'))
        m.update(bytes(self.column_name_embeddings))
        for i in self.column_embeddings.values():
            m.update(bytes(i))
        m.update(bytes(''.join(dumps(self.column_categorical)), 'utf-8')) ## does nothing
        # m.update(bytes(str(list(self.type_column.keys())) + str(list(self.type_column.values())), 'utf-8'))
        return m.digest()
        # return (
            # dumps(self.size) +
            # dumps(self.column_names) +
            # dumps(self.column_names_clean) +
            # dumps(self.column_name_embeddings) +
            # dumps(self.type_column) +
            # dumps(self.column_categorical) +
            # dumps(self.column_incomplete) +
            # dumps(self.correlated_columns) +
            # dumps(self.categorical_metadata)
    # )

    def compare_dict_of_lists(self, dictionary, other):
        if len(other) is not len(dictionary):
            return False
        for key, value in dictionary.items():
            if key in other.keys():
                if not Counter(other[key]) == Counter(value):
                    return False
            else:
                return False
        return True

    def compare_list_of_lists(self, this, other):
        if len(this) is not len(other):
            return False
        for t, o in zip(this, other):
            if not Counter(t) == Counter(o):
                return False
        return True

    def __eq__(self, other):
        to_return = (
                self.size == other.size,
                self.compare_dict_of_lists(self.column_embeddings, other.column_embeddings),
                self.compare_dict_of_lists(self.type_column, other.type_column),
                Counter(self.column_names) == Counter(other.column_names),
                Counter(self.column_names_clean) == Counter(other.column_names_clean),
                self.compare_list_of_lists(self.column_name_embeddings, other.column_name_embeddings),
                # Counter(self.column_name_embeddings) == Counter(other.column_name_embeddings),
                Counter(list(self.column_categorical)) == Counter(list(other.column_categorical)),
                Counter(list(self.column_incomplete)) == Counter(list(other.column_incomplete)),
                Counter(self.correlated_columns) == Counter(other.correlated_columns))
        return all(to_return)
    def get_column_names_by_type(self, *types):
        columns = []
        for t in types:
            columns.extend(self.type_column[t])
        return columns

    def get_numerical_columns_names(self):
        return self.get_column_names_by_type(Types.NUMERICAL, Types.FLOAT, Types.INT)

