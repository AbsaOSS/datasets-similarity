"""
This file contains constants
"""
from sentence_transformers import SentenceTransformer

from config import configure


class WarningEnable:
    """
    Class for warnings
    """
    __enable = True  # warning will be thrown if it is not True
    __timezone = "always"

    def get_status(self) -> bool:
        """
        :returns __enable
        """
        return self.__enable

    def change_status(self, status: bool):
        """
        Change __enable to status
        :param status: to be changed to
        """
        self.__enable = status

    def disable_timezone_warn(self):
        """Change timezone warning to disable"""
        self.__timezone = "ignore"

    def enable_timezone_warn(self):
        """Change timezone warning to disable"""
        self.__timezone = "always"

    def get_timezone(self) -> str:
        """
        :return: __timezone
        """
        return self.__timezone


class TrainedModel:
    """
    Class encapsulating trained module
    """
    configure()
    __model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

    def set_module(self, model: SentenceTransformer):
        """
        Sets __model
        :param model: to be set
        """
        self.__model = model

    def get_module(self) -> SentenceTransformer:
        """
        :return: __module
        """
        return self.__model


warning_enable = WarningEnable()
trained_model = TrainedModel()
