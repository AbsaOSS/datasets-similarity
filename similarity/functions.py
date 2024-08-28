"""
This module contains helpful functions
"""
import configparser
import os
import pandas as pd
from sentence_transformers import SentenceTransformer

from Column2Vec import column2vec_as_sentence, column2vec_as_sentence_clean_uniq, column2vec_as_sentence_clean, \
    column2vec_avg, column2vec_sum, column2vec_weighted_sum, column2vec_weighted_avg
from similarity.Comparator import (Comparator, SizeComparator as SizeComparatorBasic,
                                   IncompleteColumnsComparator as IncompleteColumnsComparatorBasic,
                                   KindComparator as KindComparatorBasic,
                                   ColumnNamesEmbeddingsComparator as ColumnNamesEmbeddingsComparatorBasic,
                                   ColumnExactNamesComparator as ColumnExactNamesComparatorBasic,
                                   ColumnEmbeddingComparator as ColumnEmbeddingComparatorBasic,
                                   CategoricalComparatorSimilar as CategoricalComparatorSimilarBasic)
from similarity.ComparatorByColumn import (ComparatorByColumn,
                                           SizeComparator as SizeComparatorByColumn,
                                           IncompleteColumnsComparator as IncompleteColumnsComparatorByColumn,
                                           ColumnNamesEmbeddingsComparator as ColumnNamesEmbeddingsComparatorByColumn,
                                           ColumnKindComparator as ColumnKindComparatorByColumn,
                                           ColumnExactNamesComparator as ColumnExactNamesComparatorByColumn,
                                           ColumnEmbeddingsComparator as ColumnEmbeddingsComparatorByColumn)
from similarity.DataFrameMetadata import DataFrameMetadata
from similarity.DataFrameMetadataCreator import DataFrameMetadataCreator


def load__csv_files_from_folder(folder: str) -> (list[pd.DataFrame], list[str]):
    """
    it loads cvs files from a folder and returns a list of loaded dataframe and list of names
    :param folder: from which we load the files
    :return: two lists
    """
    data = []
    names = []
    for file in os.listdir(folder):
        if file.endswith(".csv"):
            data.append(pd.read_csv(folder + "/" + file))
            names.append(file.replace(".csv", ""))
    return data, names


def create_string_from_columns(database: list[pd.DataFrame], table_names: list[str]) -> (list[str], list[str]):
    """
    For each column in each table in a database it creates string from that column.
    :param database: all tables
    :param table_names: all names of tables
    :return: list of strings representing column, list of string of the same length representing names of table for each column
    """
    sentences = []
    sentences_datasets = []
    for table, name in zip(database, table_names):
        for column in table.columns:
            sentences.append(
                str(table[column].tolist()).replace("\'", "").replace("]", "").replace("[", ""))  # column to string
            sentences_datasets.append(name)
    return sentences, sentences_datasets


def read_config() -> configparser.ConfigParser:
    """
    Read a configuration file and save it to a config object
    return: config object (config file)
    """
    config = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
    config.read_file(open('configuration.ini'))
    return config


def __get_function(name: str):
    """
    Get column2Vec function from name
    :param name: name of function
    :return: function
    """
    if name == 'sentence':
        return column2vec_as_sentence
    if name == 'sentence_clean':
        return column2vec_as_sentence_clean
    if name == 'sentence_clean_uniq':
        return column2vec_as_sentence_clean_uniq
    if name == 'avg':
        return column2vec_avg
    if name == 'sum':
        return column2vec_sum
    if name == 'weighted_sum':
        return column2vec_weighted_sum
    if name == 'weighted_avg':
        return column2vec_weighted_avg
    return None


def create_metadata(config: configparser.ConfigParser) -> list[(DataFrameMetadata, str)]:
    """
    Create metadata for all files in
    :param config: the configuration file
    :return list of metadata
    """
    data = []
    metadata = []
    if config['Input']['file'] == 'Yes':
        for file in config['Input']['path_files'].split(','):
            data.append(pd.read_csv(file))
    else:
        data, names = load__csv_files_from_folder(config['Input']['path'])
    for file, name in zip(data, names):
        metadata_creator = DataFrameMetadataCreator(file)
        metadata_creator.set_model(SentenceTransformer(config['Metadata']['model']))
        metadata_creator.set_embedding_function(__get_function(config['Embeddings']['type']))
        metadata_creator.compute_column_names_embeddings() if config['Embeddings']['names'] == 'Yes' else None
        metadata_creator.compute_column_kind() if config['Comparator']['kind'] == 'Yes' else None
        metadata_creator.create_column_embeddings() if config['Embeddings']['column'] == 'Yes' else None
        if config['Types']['type'] == 'basic':
            metadata_creator.compute_basic_types()
        if config['Types']['type'] == 'advanced':
            metadata_creator.compute_advanced_types()
        if config['Types']['type'] == 'structural':
            metadata_creator.compute_advanced_structural_types()

        metadata.append((metadata_creator.get_metadata(), name))
    return metadata


def compare(metadata: list[(DataFrameMetadata, str)], config: configparser.ConfigParser) -> pd.DataFrame():
    """
    Create comparator and compare all metadata
    :param metadata: list of metadata
    :param config: configuration file
    :return: dataframe with results
    """
    if config['Comparator']['type'] == 'basic':
        comparator = Comparator()
        types = {'size': SizeComparatorBasic(), 'incomplete': IncompleteColumnsComparatorBasic(),
                 'kind': KindComparatorBasic(), 'exact_names': ColumnExactNamesComparatorBasic(),
                 'categorical': CategoricalComparatorSimilarBasic(), 'names': ColumnNamesEmbeddingsComparatorBasic(),
                 'column': ColumnEmbeddingComparatorBasic()}
    else:
        comparator = ComparatorByColumn()
        types = {'size': SizeComparatorByColumn(), 'incomplete': IncompleteColumnsComparatorByColumn(),
                 'kind': ColumnKindComparatorByColumn(), 'exact_names': ColumnExactNamesComparatorByColumn(),
                 'names': ColumnNamesEmbeddingsComparatorByColumn(), 'column': ColumnEmbeddingsComparatorByColumn()}

    if config['Comparator']['size'] == 'Yes':
        comparator.add_comparator_type(types['size'])
    if config['Comparator']['incomplete'] == 'Yes':
        comparator.add_comparator_type(types['incomplete'])
    if config['Comparator']['kind'] == 'Yes':
        comparator.add_comparator_type(types['kind'])
    if config['Comparator']['exact_names'] == 'Yes':
        comparator.add_comparator_type(types['exact_names'])
    if config['Comparator']['categorical'] == 'Yes' and config['Comparator']['type'] == 'basic':
        comparator.add_comparator_type(types['categorical'])
    if config['Embeddings']['names'] == 'Yes':
        comparator.add_comparator_type(types['names'])
    if config['Embeddings']['column'] == 'Yes':
        comparator.add_comparator_type(types['column'])

    comparator_res = pd.DataFrame()
    for met1, name1 in metadata:
        for met2, name2 in metadata:
            comparator_res.loc[name1, name2] = comparator.compare(met1, met2)
    return comparator_res
