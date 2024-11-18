"""
File contains Connector interface
"""

import abc
from typing import Any

from src.models.connector_models import ConnectorSettings
from src.models.metadata import MetadataCreatorInput


class ConnectorInterface(metaclass=abc.ABCMeta):
    """
    ConnectorInterface class is an abstract class that defines
     the methods that must be implemented by the concrete connector classes.
    """

    @abc.abstractmethod
    def _connect_and_load_data_source(self, settings: ConnectorSettings) -> Any:
        """Load the data set
        :param settings: ConnectorSettings for getting information about files
        this is a protected method"""
        raise NotImplementedError

    @abc.abstractmethod
    def _format_data(self, data: Any) -> list[MetadataCreatorInput]:
        """Format loaded data
        this is a protected method"""
        raise NotImplementedError

    def close(self):
        """Close the connection"""
        pass

    def get_data(self, settings: ConnectorSettings) -> list[MetadataCreatorInput]:
        """Get formated data from the loaded data source
        :return: data"""
        data = self._connect_and_load_data_source(settings)
        return self._format_data(data)

