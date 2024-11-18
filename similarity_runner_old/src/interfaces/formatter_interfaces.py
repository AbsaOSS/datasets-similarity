"""
This file contains abstract class OutputFormaterInterface
"""

import abc


class OutputFormaterInterface(metaclass=abc.ABCMeta):
    """
    OutputFormaterInterface class is an abstract interface that defines
     the methods that must be implemented by the concrete formater classes.
    """

    @abc.abstractmethod
    def format(self, data: dict):
        """Format data to specific format"""
