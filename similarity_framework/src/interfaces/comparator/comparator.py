from abc import abstractmethod, ABC

from similarity_framework.src.interfaces.common import DistanceFunction
from similarity_framework.src.impl.comparator.distance_functions import HausdorffDistanceMin
from similarity_framework.src.interfaces.comparator.handler import HandlerType
from similarity_framework.src.models.metadata import Metadata
from similarity_framework.src.models.similarity import Settings, SimilarityOutput
from similarity_framework.src.models.settings import AnalysisSettings

class Comparator(ABC):
    """
    Abstract Comparator class
    """

    def __init__(self):
        self.settings: set[Settings] = set()
        self.distance_function = HausdorffDistanceMin()
        self.comparator_type: list[HandlerType] = []
        self.analysis_settings: AnalysisSettings = None

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

    def compare(self, metadata1: Metadata, metadata2: Metadata, analysis_settings: AnalysisSettings = AnalysisSettings()) -> SimilarityOutput:
        self.analysis_settings = analysis_settings
        self.__pre_compare()
        return self._compare(metadata1, metadata2)

    def __pre_compare(self):
        for i in self.comparator_type:
            i.settings = self.settings
            i.analysis_settings = self.analysis_settings
        self.__pre_compare_individual()

    def __pre_compare_individual(self, **kwargs):
        """This method can be implemented by each implementation and will be called automatically at __pre_compare method"""

    @abstractmethod
    def add_comparator_type(self, comparator: HandlerType) -> "Comparator":
        pass

    @staticmethod
    @abstractmethod
    def from_settings(settings: AnalysisSettings) -> "Comparator":
        pass

    @abstractmethod
    def _compare(self, metadata1: Metadata, metadata2: Metadata) -> SimilarityOutput:
        """
        Compare two tables according to previously set properties.
        """
