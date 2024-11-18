"""
This file contains JSON formater implementation.
"""

import json

from src.interfaces.formatter_interfaces import OutputFormaterInterface


class JsonFormater(OutputFormaterInterface):
    """
    This class is responsible for formatting the output in JSON format.
    """

    def format(self, data: dict) -> str:
        """
        Format data to JSON
        :param data: dict data to format
        :return: json formatted data in str
        """
        json_data = json.dumps(data, indent=4)
        return json_data
