from abc import ABC, abstractmethod

import pandas as pd

from similarity_framework.src.models.metadata import Metadata
from similarity_framework.src.models.settings import AnalysisSettings


class HandlerType(ABC):
    """Abstract class for comparators"""

    def __init__(self, weight: int = 1, analysis_settings: AnalysisSettings = None):
        """
        Constructor for ComparatorType
        :param weight: weight of the comparator
        """
        self.weight: int = weight
        self.analysis_settings: AnalysisSettings = analysis_settings

    @abstractmethod
    def compare(self, metadata1: Metadata, metadata2: Metadata, **kwargs) -> pd.DataFrame | float:
        """This method should compare two tables and return distance table"""
