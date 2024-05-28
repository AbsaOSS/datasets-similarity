"""
The main.py contains example usage.
You can run program to compare tables by main
"""
import sys

import pandas as pd

from constants import warning_enable
from similarity.Comparator import (Comparator, SizeComparator,
                                   IncompleteColumnsComparator, KindComparator,
                                   ColumnNamesEmbeddingsComparator)
from similarity.ComparatorByColumn import (ComparatorByColumn, SizeComparator,
                                           IncompleteColumnsComparator,
                                           ColumnNamesEmbeddingsComparator)
from similarity.DataFrameMetadataCreator import DataFrameMetadataCreator


def create_metadata(data):
    """
    This function creates metadata
    :return created metadata
    """
    return (DataFrameMetadataCreator(data).
            compute_advanced_structural_types().
            compute_column_kind().compute_column_names_embeddings()).get_metadata()


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
    comparator2 = (ComparatorByColumn().add_comparator_type(SizeComparator()).
                   add_comparator_type(IncompleteColumnsComparator())
                   .add_comparator_type(ColumnNamesEmbeddingsComparator()))
    compartor = (Comparator().add_comparator_type(SizeComparator()).
                 add_comparator_type(IncompleteColumnsComparator())
                 .add_comparator_type(KindComparator())
                 .add_comparator_type(ColumnNamesEmbeddingsComparator()))
    # return compartor.compare(metadata1, metadata2)
    return comparator2.compare(metadata1, metadata2)


if __name__ == '__main__':
    warning_enable.change_status(False)
    warning_enable.disable_timezone_warn()
    files = sys.argv[1:]
    print(files)
    for file1 in files:
        for file2 in files:
            if file1 != file2:
                distance = compare_datasets(file1, file2)
                print(f"{file1} |< >| {file2} = {distance}")
    if len(files) == 0:
        distance = compare_datasets('data/netflix_titles.csv', 'data/imdb_top_1000.csv')
        print(f"'data/netflix_titles.csv' |< >| 'data/imdb_top_1000.csv' = {distance}")
