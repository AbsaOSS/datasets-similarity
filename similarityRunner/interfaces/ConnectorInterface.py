"""
File contains Connector interface
"""
import abc

from models.connector_models import ConnectorSettings, Output, ConnectorOutput


class ConnectorInterface(metaclass=abc.ABCMeta):
    """
    ConnectorInterface class is an abstract class that defines
     the methods that must be implemented by the concrete connector classes.
    """

    @abc.abstractmethod
    def _connect_and_load_data_source(self, settings: ConnectorSettings) -> ConnectorOutput:
        """Load in the data set
        :param settings: ConnectorSettings
        this is a protected method"""
        raise NotImplementedError

    @abc.abstractmethod
    def _format_data(self, data: ConnectorOutput) -> Output:
        """Format loaded data
        this is a protected method"""
        raise NotImplementedError

    def get_data(self, settings: ConnectorSettings) -> Output:
        """Get formated data from the loaded data source
        :return: data"""
        data = self._connect_and_load_data_source(settings)
        return self._format_data(data)
