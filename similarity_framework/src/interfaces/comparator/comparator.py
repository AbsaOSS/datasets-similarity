from abc import abstractmethod, ABC

import pandas as pd

from src.interfaces.common import DistanceFunction
from src.interfaces.comparator.distance_functions import HausdorffDistanceMin
from src.models.metadata import Metadata
from src.models.models import Settings


class HandlerType(ABC):
    """Abstract class for comparators"""

    def __init__(self, weight: int = 1):
        # TODO:KUBA settings se musi pridat do vsech construktoru
        """
        Constructor for ComparatorType
        :param weight: weight of the comparator
        """
        self.weight: int = weight

    @abstractmethod
    def compare(self, metadata1: Metadata, metadata2: Metadata, **kwargs) -> pd.DataFrame | float:
        """This method should compare two tables and return distance table"""


class Comparator(ABC):
    """
    Abstract Comparator class
    """

    def __init__(self):
        self.settings: set[Settings] = set()
        self.distance_function = HausdorffDistanceMin()
        self.comparator_type: list[HandlerType] = []

    def set_distance_function(self, distance_function: DistanceFunction) -> "Comparator":
        """
        Set distance function for comparing two tables
        """
        self.distance_function = distance_function
        return self

    def set_settings(self, settings: set) -> "Comparator":
        """
        Set settings for comparing two tables
        """
        self.settings = settings
        return self

    def add_settings(self, setting: Settings) -> "Comparator":
        """
        Add another setting for comparing two tables
        """
        self.settings.add(setting)
        return self

    def compare(self, metadata1: Metadata, metadata2: Metadata) -> float:
        self.__pre_compare()
        return self._compare(metadata1, metadata2)

    def __pre_compare(self):
        for i in self.comparator_type:
            i.settings = self.settings
        self.__pre_compare_individual()

    def __pre_compare_individual(self, **kwargs):
        """This method can be implemented by each implementation and will be called automatically at __pre_compare method"""
        pass

    @abstractmethod
    def add_comparator_type(self, comparator: HandlerType) -> "Comparator":
        pass

    @abstractmethod
    def _compare(self, metadata1: Metadata, metadata2: Metadata) -> float:
        """
        Compare two tables according to previously set properties.
        """
        pass
