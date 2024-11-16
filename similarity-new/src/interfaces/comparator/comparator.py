from abc import abstractmethod, ABC

import pandas as pd

from src.interfaces.common import DistanceFunction
from src.interfaces.comparator.distance_functions import HausdorffDistanceMin
from src.models.metadata import DataFrameMetadata
from src.models.models import Settings


class HandlerType(ABC):
    """Abstract class for comparators"""

    def __init__(self, settings: set[Settings], weight: int = 1):
        # TODO:KUBA settings se musi pridat do vsech construktoru
        """
        Constructor for ComparatorType
        :param weight: weight of the comparator
        """
        self.weight: int = weight
        self.settings: set[Settings] = settings

    @abstractmethod
    def compare(self, metadata1: DataFrameMetadata, metadata2: DataFrameMetadata, **kwargs) -> pd.DataFrame:
        """This method should compare two tables and return distance table"""


class Comparator(ABC):
    """
    Abstract Comparator class
    """

    def __init__(self):
        # self.comparator_type: list[HandlerType] = []
        self.settings: set[Settings] = set()
        self.distance_function = HausdorffDistanceMin()

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

    def add_comparator_type(self, comparator: HandlerType) -> "Comparator":
        pass

    def compare(self, metadata1: DataFrameMetadata, metadata2: DataFrameMetadata) -> float:
        """
        Compare two tables according to previously set properties.
        """
