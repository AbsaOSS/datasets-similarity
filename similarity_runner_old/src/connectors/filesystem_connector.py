"""
This file contains filesystem connector implementation
"""

import os

from src.functions_runner import load_files_from_list
from src.interfaces.connector_interfaces import ConnectorInterface
from src.models.connector_models import Output, ConnectorOutput, FSConnectorSettings


class FilesystemConnector(ConnectorInterface):
    """
    FilesystemConnector class is a class that implements ConnectorInterface.
    It is used to load data from filesystem
    """

    def _connect_and_load_data_source(self, settings: FSConnectorSettings) -> ConnectorOutput:
        """
        Load data by settings from filesystem
        :param settings: FSConnectorSettings with paths and file type
        :return: ConnectorOutput with loaded tables and names
        """
        file_list = settings.files_paths
        for folder in settings.directory_paths:
            file_list = file_list + [os.path.join(folder, s) for s in os.listdir(folder)]

        tables, names = load_files_from_list(file_list, settings.file_type)
        return ConnectorOutput(names=names, tables=tables)

    def _format_data(self, data: ConnectorOutput) -> Output:
        """
        Format loaded data to Output format
        """
        return data.tables, data.names

    def close(self):
        """
        Close the connection in this case it is unnecessary
        """
