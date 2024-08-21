"""
The main.py contains example usage.
You can run program to compare tables by main
"""
import configparser
import sys

import pandas as pd

from arg_parser import init_args, parse_args
from constants import warning_enable
from similarity.Comparator import (Comparator, SizeComparator,
                                   IncompleteColumnsComparator, KindComparator,
                                   ColumnNamesEmbeddingsComparator)
from similarity.ComparatorByColumn import (ComparatorByColumn, SizeComparator,
                                           IncompleteColumnsComparator,
                                           ColumnNamesEmbeddingsComparator)
from similarity.DataFrameMetadata import DataFrameMetadata
from similarity.DataFrameMetadataCreator import DataFrameMetadataCreator


def create_metadata_basic(data):
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
    metadata1 = create_metadata_basic(data1)
    metadata2 = create_metadata_basic(data2)
    comparator2 = (ComparatorByColumn().add_comparator_type(SizeComparator()).
                   add_comparator_type(IncompleteColumnsComparator()).
                   add_comparator_type(ColumnNamesEmbeddingsComparator()))
    compartor = (Comparator().add_comparator_type(SizeComparator()).
                 add_comparator_type(IncompleteColumnsComparator()).
                 add_comparator_type(KindComparator()).
                 add_comparator_type(ColumnNamesEmbeddingsComparator()))
    # return compartor.compare(metadata1, metadata2)
    return comparator2.compare(metadata1, metadata2)


def test():
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


def read_config() -> configparser.ConfigParser:
    """
    Read a configuration file and save it to a config object
    """
    config = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
    config.read_file(open('configuration.ini'))
    return config


def create_metadata(config: configparser.ConfigParser) -> list[(DataFrameMetadata, str)]:
    """
    Create metadata for all files in the configuration
    """
    data = []
    metadata = []
    if config['Input']['file'] == 'Yes':
        for file in config['Input']['path_files'].split(','):
            data.append(pd.read_csv(file))
    else:
        ...  # todo read data from dir
    for file in data:
        metadata_creator = DataFrameMetadataCreator(file)
        # todo set metadata acording to config
        metadata.append((metadata_creator.get_metadata(), file))
    return metadata


def compare(metadata: list[(DataFrameMetadata, str)], config: configparser.ConfigParser) -> dict:
    comparator = Comparator()
    comparator_res = {}
    if config['Comparator']['size'] == 'Yes':
        comparator.add_comparator_type(SizeComparator())
    if config['Comparator']['incomplete'] == 'Yes':
        comparator.add_comparator_type(IncompleteColumnsComparator())
    if config['Comparator']['kind'] == 'Yes':
        comparator.add_comparator_type(KindComparator())
    if config['Comparator']['exact_names'] == 'Yes':
        comparator.add_comparator_type(ColumnNamesEmbeddingsComparator())

    # todo the byColumn comparator all settings

    for met1, name1 in metadata:
        for met2, name2 in metadata:
            comparator_res[name1][name2] = comparator.compare(met1, met2) #todo init dict


def print_res(comparator_result: dict):
    ...


def similarity_run():
    config = read_config()
    metadata = create_metadata(config)
    comparator_res = compare(metadata, config)
    print_res(comparator_res)


if __name__ == '__main__':
    # test()
    args = sys.argv[1:]
    if len(args) == 0:
        similarity_run()
    else:
        parse_args(init_args())
        similarity_run()
