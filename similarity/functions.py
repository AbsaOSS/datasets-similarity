"""
This module contains helpful functions
"""
import os
import pandas as pd


def load__csv_files_from_folder(folder: str) -> (list[pd.DataFrame], list[str]):
    """
    it loads cvs files from folder and returns list of loaded dataframe and list of names
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
    For each column in each table in database it creates string from that column.
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
