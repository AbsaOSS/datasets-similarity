"""
This file contains filesystem connector implementation
"""
import os

from functionsRunner import load_files_from_list
from interfaces.ConnectorInterface import ConnectorInterface
from models.connector_models import ConnectorSettings, Output, ConnectorOutput, FSConnectorSettings


class FilesystemConnector(ConnectorInterface):
    def __init__(self, config):
        self.config = config

    def _connect_and_load_data_source(self, settings: FSConnectorSettings) -> ConnectorOutput:
        file_list = settings.files_paths
        for folder in settings.directory_paths:
            file_list = file_list + [folder + "/" +  s for s in os.listdir(folder)]

        names, tables = load_files_from_list(os.listdir(file_list), settings.file_type)
        return ConnectorOutput(names=names, tables=tables)

    def _format_data(self, data: ConnectorOutput) -> Output:
        pass

    def close(self):
        pass

