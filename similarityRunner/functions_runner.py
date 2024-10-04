"""
This file contains functions used in the similarityRunner package.
"""

import pandas as pd

from models.connector_models import FileType


def load_files_from_list(folder: list[str], file_types: tuple = (FileType.CSV,)) -> tuple[list[pd.DataFrame], list[str]]:
    """
    Load files from a list of file
    :param folder: list of files to load
    :param file_types: tuple of possible file types
    :return: tuple of data list and names list
    """
    data = []
    names = []
    for file in folder:
        if FileType.CSV in file_types and file.endswith(".csv"):
            data.append(pd.read_csv(file))
            names.append(file.replace(".csv", ""))
        if FileType.PARQUET in file_types and file.endswith(".parquet"):
            data.append(pd.read_parquet(file))
            names.append(file.replace(".parquet", ""))
    return data, names


def csv_to_parquet(file: str) -> str:
    """
    Convert csv file to parquet
    :param file: file to convert
    """
    df = pd.read_csv(file)
    df.to_parquet(file.replace(".csv", ".parquet"))
    return file.replace(".csv", ".parquet")
