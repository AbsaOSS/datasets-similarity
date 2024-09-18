"""
File contains UserInterface interface
"""
import abc

from models.user_models import SimilarityOutput
from models.connector_models import ConnectorSettings


class UserInterface(metaclass=abc.ABCMeta):
    """
    UserInterface is an abstract class that defines the methods
     that must be implemented by any class that inherits from it.
    """

    @abc.abstractmethod
    def get_user_input(self) -> ConnectorSettings:
        """
        Get user input and returns it as ConnectorSettings object
        """
        raise NotImplementedError

    @abc.abstractmethod
    def display_output(self, output: SimilarityOutput) -> None:
        """
        Display output to the user
        """
        raise NotImplementedError
