"""
The main.py contains example usage.
You can run program to compare tables by main
"""

import sys

import pandas as pd
import logging

from similarity_framework.config import configure
from similarity_framework.src.impl.comparator.comparator_by_type import ComparatorByType, IncompleteColumnsHandler, ColumnNamesEmbeddingsHandler
from similarity_framework.src.impl.comparator.comparator_by_column import (
    ComparatorByColumn,
    IncompleteColumnsHandler as IncompleteColumnsComparatorByColumn,
    ColumnNamesEmbeddingsHandler as ColumnNamesEmbeddingsComparatorByColumn,
)
from similarity_framework.src.impl.metadata.type_metadata_creator import TypeMetadataCreator

BY_COLUMN = True
configure()


def create_metadata(data):
    return (TypeMetadataCreator().compute_advanced_structural_types().compute_column_kind().compute_column_names_embeddings()).get_metadata(data)


def compare_datasets(path1: str, path2):
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
        ## different option
        # .add_comparator_type(SizeComparatorByColumn())
        .add_comparator_type(IncompleteColumnsComparatorByColumn()).add_comparator_type(ColumnNamesEmbeddingsHandler())
        ## different option
        # .add_comparator_type(ColumnKindHandler())
    )
    compartor = (
        ComparatorByType()
        ## different option
        # .add_comparator_type(SizeHandler())
        .add_comparator_type(IncompleteColumnsHandler())
        ## different option
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
    logging.info(f"'{path1}' |< >| '{path2}' = {distance}\n")


if __name__ == "__main__":
    configure()

    files = sys.argv[1:]
    logging.info(files)
    for file1 in files:
        for file2 in files:
            if file1 != file2:
                distance = compare_datasets(file1, file2).distance
                logging.info(f"{file1} |< >| {file2} = {distance}")
    if len(files) == 0:
        comapre_two("data/netflix_titles.csv", "data/netflix_titles.csv")
        comapre_two("data/netflix_titles.csv", "data/netflix_titles_half.csv")
        comapre_two("data/netflix_titles.csv", "data/netflix_titles_without_column.csv")
        comapre_two("data/netflix_titles.csv", "data/imdb_top_1000.csv")
