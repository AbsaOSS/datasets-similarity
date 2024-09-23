"""
This file contains filesystem connector implementation
"""
import os

from functionsRunner import load_files_from_list
from interfaces.ConnectorInterface import ConnectorInterface
from models.connector_models import Output, ConnectorOutput, FSConnectorSettings


class FilesystemConnector(ConnectorInterface):

    def _connect_and_load_data_source(self, settings: FSConnectorSettings) -> ConnectorOutput:
        file_list = settings.files_paths
        for folder in settings.directory_paths:
            file_list = file_list + [os.path.join(folder, s) for s in os.listdir(folder)]

        tables, names = load_files_from_list(file_list, settings.file_type)
        return ConnectorOutput(names=names, tables=tables)

    def _format_data(self, data: ConnectorOutput) -> Output:
        return data.tables, data.names

    def close(self):
        pass
