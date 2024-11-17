from abc import ABC, abstractmethod

import pandas as pd


class DistanceFunction(ABC):
    """Abstract class for distance classes"""

    @abstractmethod
    def compute(self, distance_table: pd.DataFrame):
        """Method should compute overall distance from distance_table"""
