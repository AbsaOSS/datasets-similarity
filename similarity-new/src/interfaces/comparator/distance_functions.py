import numpy as np
import pandas as pd

from src.interfaces.common import DistanceFunction


class HausdorffDistanceMin(DistanceFunction):
    """Hausdorff distance class"""

    def compute(self, distance_table: pd.DataFrame) -> float:
        """
        Compute Hausdorff distance with min function.
        :param distance_table:  dataframe
        :return: float between 0 and 1
        """
        if distance_table.size == 0:
            return np.nan
        row_mins = distance_table.min(axis=1)
        column_mins = distance_table.min(axis=0)
        return min(row_mins.max(), column_mins.max())
