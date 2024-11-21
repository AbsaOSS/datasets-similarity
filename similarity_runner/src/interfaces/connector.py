import abc
from typing import Any, ClassVar

from similarity_framework.src.models.metadata import MetadataCreatorInput
from similarity_runner.src.models.connectors import ConnectorSettings


class ConnectorInterface(abc.ABC):
    """
    ConnectorInterface class is an abstract class that defines
     the methods that must be implemented by the concrete connector classes.
    """

    @staticmethod
    @abc.abstractmethod
    def get_settings_class() -> type[ConnectorSettings]:
        """Get the settings class for the connector
        this is a static method"""
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def get_name() -> str:
        """Get the name of the connector
        this is a static method"""
        raise NotImplementedError

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
