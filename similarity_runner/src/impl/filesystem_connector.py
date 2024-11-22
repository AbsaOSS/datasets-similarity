"""
This file contains filesystem connector implementation
"""

import os
from typing import Iterable, ClassVar

import pandas as pd

from similarity_framework.src.models.metadata import MetadataCreatorInput
from similarity_runner.src.interfaces.connector import ConnectorInterface
from similarity_runner.src.models.connectors import FSConnectorSettings, FileType, ConnectorSettings


def load_files_from_list(files: list[str], file_types: Iterable[FileType] = (FileType.CSV,)) -> list[MetadataCreatorInput]:
    """
    Load files from a list of file
    :param folder: list of files to load
    :param file_types: tuple of possible file types
    :return: tuple of data list and names list
    """
    result = []
    for file in files:
        if FileType.CSV in file_types and file.endswith(".csv"):
            result.append(MetadataCreatorInput(dataframe=pd.read_csv(file), source_name=file.replace(".csv", "")))
        if FileType.PARQUET in file_types and file.endswith(".parquet"):
            result.append(MetadataCreatorInput(dataframe=pd.read_parquet(file), source_name=file.replace(".parquet", "")))
    return result


class FilesystemConnector(ConnectorInterface):
    """
    FilesystemConnector class is a class that implements ConnectorInterface.
    It is used to load data from filesystem
    """

    @staticmethod
    def get_settings_class() -> type[FSConnectorSettings]:
        return FSConnectorSettings

    @staticmethod
    def get_name():
        return "filesystem"

    def _connect_and_load_data_source(self, settings: FSConnectorSettings) -> list[MetadataCreatorInput]:
        """
        Load data by settings from filesystem
        :param settings: FSConnectorSettings with paths and file type
        :return: ConnectorOutput with loaded tables and names
        """
        file_list = settings.files_paths
        for folder in settings.directory_paths:
            file_list = file_list + [os.path.join(folder, s) for s in os.listdir(folder)]

        return __load_files_from_list(file_list, settings.filetypes)

    def _format_data(self, data: list[MetadataCreatorInput]) -> list[MetadataCreatorInput]:
        """
        Format loaded data to Output format
        """
        return data

    def close(self):
        """
        Close the connection in this case it is unnecessary
        """
        pass
