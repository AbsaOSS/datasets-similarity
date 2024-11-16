"""
The main.py contains example usage.
You can run program to compare tables by main
"""

import sys

import pandas as pd

from config import configure
from constants import warning_enable
from similarity_framework.src.impl.comparator.comparator_by_type import ComparatorByType, IncompleteColumnsHandler, SizeHandler, ColumnNamesEmbeddingsHandler, KindHandler
from similarity_framework.src.impl.comparator.comparator_by_column import (ComparatorByColumn, SizeHandler as SizeComparatorByColumn, IncompleteColumnsHandler as IncompleteColumnsComparatorByColumn,
                                                                           ColumnNamesEmbeddingsHandler as ColumnNamesEmbeddingsComparatorByColumn, ColumnKindHandler)
from similarity_framework.src.impl.metadata.type_metadata_creator import TypeMetadataCreator
BY_COLUMN = True
configure()


def create_metadata(data):
    """
    This function creates metadata
    :return created metadata
    """
    return (TypeMetadataCreator(data).compute_advanced_structural_types().compute_column_kind().compute_column_names_embeddings()).get_metadata()


def compare_datasets(path1, path2):
    """
    This function compare two tables
    It will read datasets, create metadata and comparator, compare them
    :param path1: to file with table 1
    :param path2: to file with table 2
    :return: distance between tables
    """
    data1 = pd.read_csv(path1)
    data2 = pd.read_csv(path2)
    metadata1 = create_metadata(data1)
    metadata2 = create_metadata(data2)
    comparator_by_column = (
        ComparatorByColumn()
            # .add_comparator_type(SizeComparatorByColumn())
            .add_comparator_type(IncompleteColumnsComparatorByColumn())
            .add_comparator_type(ColumnNamesEmbeddingsComparatorByColumn())
            # .add_comparator_type(ColumnKindHandler())
    )
    compartor = (
        ComparatorByType()
            # .add_comparator_type(SizeHandler())
            .add_comparator_type(IncompleteColumnsHandler())
            # .add_comparator_type(KindHandler())
            .add_comparator_type(ColumnNamesEmbeddingsHandler())
    )
    if BY_COLUMN:
        return comparator_by_column.compare(metadata1, metadata2)
    return compartor.compare(metadata1, metadata2)


def comapre_two(path1, path2):
    """
    This function compare two tables
    It will read datasets, create metadata and comparator, compare them
    :param path1: to file with table 1
    :param path2: to file with table 2
    :return: distance between tables
    """
    distance = compare_datasets(
        path1,
        path2,
    ).distance
    print(f"'{path1}' |< >| '{path2}' = {distance}\n")

if __name__ == "__main__":
    configure()
    warning_enable.change_status(False)
    warning_enable.disable_timezone_warn()

    comapre_two("data/netflix_titles.csv", "data/netflix_titles.csv")
    comapre_two("data/netflix_titles.csv", "data/netflix_titles_half.csv")
    comapre_two("data/netflix_titles.csv", "data/netflix_titles_without_column.csv")
    comapre_two("data/netflix_titles.csv", "data/imdb_top_1000.csv")

    # files = sys.argv[1:]
    # print(files)
    # for file1 in files:
    #     for file2 in files:
    #         if file1 != file2:
    #             distance = compare_datasets(file1, file2).distance
    #             print(f"{file1} |< >| {file2} = {distance}")
    # if len(files) == 0:
    #     distance = compare_datasets(
    #         "data/netflix_titles.csv",
    #         "data/netflix_titles.csv",
    #         # "data/imdb_top_1000.csv",
    #     ).distance
    #     print(f"'data/netflix_titles.csv' |< >| 'data/imdb_top_1000.csv' = {distance}")
