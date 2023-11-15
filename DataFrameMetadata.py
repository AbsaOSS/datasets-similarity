from collections import defaultdict

from Types import Types


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

    def get_column_names_by_type(self, *types):
        columns = []
        for t in types:
            columns.extend(self.type_column[t])
        return columns

    def get_numerical_columns_names(self):
        return self.get_column_names_by_type(Types.NUMERICAL, Types.FLOAT, Types.INT)


    #
    # def __getattribute__(self, __name):
    #     return super().__getattribute__(__name)
    #
    # def __setattr__(self, __name, __value):
    #     super().__setattr__(__name, __value)



