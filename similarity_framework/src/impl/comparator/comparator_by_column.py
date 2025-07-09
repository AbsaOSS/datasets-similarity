import numpy as np
import pandas as pd


from similarity_framework.src.impl.comparator.distance_functions import HausdorffDistanceMin, AverageDist
from similarity_framework.src.impl.comparator.handlers import (
    SizeHandler,
    IncompleteColumnsHandler,
    ColumnExactNamesHandler,
    ColumnNamesEmbeddingsHandler,
    ColumnEmbeddingsHandler,
    ColumnKindHandler,
    ColumnTypeHandler,
    TableHandler,
)
from similarity_framework.src.interfaces.comparator.comparator import HandlerType, Comparator
from similarity_framework.src.models.metadata import Metadata
from similarity_framework.src.models.similarity import SimilarityOutput
from similarity_framework.src.models.settings import AnalysisSettings


class ComparatorByColumn(Comparator):
    """
    Comparator for comparing two tables
    """

    @staticmethod
    def from_settings(settings: AnalysisSettings) -> "ComparatorByColumn":
        comparator = ComparatorByColumn()
        if settings.size:
            comparator.add_comparator_type(SizeHandler(settings.weights.size))
        if settings.incomplete_columns:
            comparator.add_comparator_type(IncompleteColumnsHandler(settings.weights.incomplete_columns))
        if settings.exact_names:
            comparator.add_comparator_type(ColumnExactNamesHandler(settings.weights.exact_names))
        if settings.column_name_embeddings:
            comparator.add_comparator_type(ColumnNamesEmbeddingsHandler(settings.weights.column_name_embeddings))
        if settings.column_embeddings:
            comparator.add_comparator_type(ColumnEmbeddingsHandler(settings.weights.column_embeddings))
        if settings.kinds:
            comparator.add_comparator_type(ColumnKindHandler(weight=settings.weights.kinds))
        if settings.type_basic or settings.type_structural or settings.type_advanced:
            comparator.add_comparator_type(ColumnTypeHandler(settings.weights.type))
        if settings.distance_function:
            func = HausdorffDistanceMin() if settings.distance_function == "HausdorffDistanceMin" else AverageDist()
            comparator.set_distance_function(func)
        return comparator

    def __init__(self):
        """
        Constructor for ComparatorByColumn
        """
        super().__init__()
        self.table_comparators: list[TableHandler] = []

    def add_comparator_type(self, comparator: HandlerType) -> "ComparatorByColumn":
        """
        Add comparator
        """
        # todo if comparator contains type and kind comparator change it to kind_and_tyep_comparator
        if isinstance(comparator, TableHandler):
            self.table_comparators.append(comparator)
        else:
            self.comparator_type.append(comparator)
        return self

    def weightwed_avg(self, distances: list[tuple[float, int]]) -> float:
        """
        Compute weighted average of distances
        :param distances: list of tuples (distance, weight)
        :return: weighted average
        """
        sum_weight = sum([weight for _, weight in distances if not np.isnan(weight)])
        return sum([distance * weight / sum_weight for distance, weight in distances if not np.isnan(distance)])

    def __pre_compare_individual(self):
        for i in self.table_comparators:
            i.settings = self.settings
            i.analysis_settings = self.analysis_settings

    def _compare(self, metadata1: Metadata, metadata2: Metadata) -> SimilarityOutput:
        """
        Compare two tables according to previously set properties.
        """

        table_distances = []
        distances = pd.DataFrame()
        for comparator in self.table_comparators:
            table_distances.append(comparator.compare(metadata1, metadata2))
        if self.comparator_type:
            for column1 in metadata1.column_names:
                for column2 in metadata2.column_names:
                    comparators_distances = []
                    for comparator in self.comparator_type:
                        comparators_distances.append(
                            (
                                comparator.compare(
                                    metadata1,
                                    metadata2,
                                    index1=column1,
                                    index2=column2,
                                ),
                                comparator.weight,
                            )
                        )
                    distances.loc[column1, column2] = self.weightwed_avg(comparators_distances)
            res = self.distance_function.compute(distances)
            res = res * res
        else:
            res = 1
        if table_distances:
            for dist in table_distances:
                res += dist * dist
        return SimilarityOutput(distance=np.sqrt(res / 2))
