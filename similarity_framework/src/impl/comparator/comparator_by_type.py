from __future__ import annotations

import math
from statistics import mean

import numpy as np
import pandas as pd
from torch import Tensor

from logging_ import logger
from similarity_framework.src.impl.comparator.comparator_by_column import ColumnTypeHandler, IncompleteColumnsHandler, ColumnExactNamesHandler, \
    ColumnNamesEmbeddingsHandler, ColumnEmbeddingsHandler, SizeHandler, ColumnKindHandler
from similarity_framework.src.impl.comparator.utils import cosine_sim, get_ratio, concat, fill_result
from similarity_framework.src.interfaces.common import DistanceFunction
from similarity_framework.src.impl.comparator.distance_functions import HausdorffDistanceMin, AverageDist
from similarity_framework.src.interfaces.comparator.comparator import HandlerType, Comparator
from similarity_framework.src.models.metadata import Metadata
from similarity_framework.src.models.similarity import SimilarityOutput, Settings
from similarity_framework.src.models.types_ import DataKind, Type
from similarity_framework.src.models.settings import AnalysisSettings


class ComparatorByType(Comparator):
    """
    Comparator for comparing two tables by type
    """

    @staticmethod
    def from_settings(settings: AnalysisSettings) -> "ComparatorByType":
        comparator = ComparatorByType()
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
            comparator.set_kinds(True)
            comparator.kind_weight = settings.weights.kinds
        if settings.type_basic or settings.type_structural or settings.type_advanced:
            comparator.set_types(True)
            comparator.type_weight = settings.weights.type
        if settings.distance_function:
            func = HausdorffDistanceMin() if settings.distance_function == "HausdorffDistanceMin" else AverageDist()
            comparator.set_distance_function(func)
        logger.info("Comparator by type created")
        logger.info(f"Handlers used: {','.join([item.__class__.__name__ for item in comparator.comparator_type])}")
        return comparator

    def __init__(self):
        super().__init__()
        self.kinds = False
        self.types = False
        self.kinds_compare = True
        self.types_compare = True
        self.kind_weight = 1
        self.type_weight = 1
    def set_kinds(self, value: bool) -> "ComparatorByType":
        """
        Set if kinds should be compared
        """
        self.kinds = value
        return self

    def set_types(self, value: bool) -> "ComparatorByType":
        """
        Set if types should be compared
        """
        self.types = value
        return self

    def add_comparator_type(self, comparator: HandlerType) -> "ComparatorByType":
        """
        Add comparator
        """
        self.comparator_type.append(comparator)
        return self

    def __compare_all_columns(self, metadata1: Metadata, metadata2: Metadata,
                                 column_names1: set[str], column_names2: set[str],
                                 comparators: list[HandlerType]) -> pd.DataFrame:
        all_compares = []
        for comparator in comparators:
            col_to_col = pd.DataFrame()
            for idx1, name1 in enumerate(column_names1):
                for idx2, name2 in enumerate(column_names2):
                    result = comparator.compare(metadata1, metadata2, index1=name1, index2=name2)
                    if result is not np.nan:
                        col_to_col.loc[idx1, idx2] = result
            if not col_to_col.empty: all_compares.append(col_to_col) # todo add , comparator.weight
        return pd.DataFrame if all_compares == [] else concat(*all_compares)

    def __compare_types(self, type_, metadata1: Metadata, metadata2: Metadata) -> pd.DataFrame:
        comparators = self.comparator_type.copy()
        if self.types_compare: comparators.append(ColumnTypeHandler())
        all_compares = self.__compare_all_columns(metadata1, metadata2,
                                                  metadata1.column_type[type_],
                                                  metadata2.column_type[type_],
                                                  comparators)
        return all_compares

    def __compare_kinds(self, kind, metadata1: Metadata, metadata2: Metadata) -> pd.DataFrame:
        comparators = self.comparator_type.copy()
        if self.kinds_compare: comparators.append(ColumnKindHandler())
        all_compares = self.__compare_all_columns(metadata1, metadata2,
                                                  metadata1.column_kind[kind],
                                                  metadata2.column_kind[kind],
                                                  comparators)
        return all_compares

    def _compare(self, metadata1: Metadata, metadata2: Metadata) -> SimilarityOutput:
        """
        Compare two tables according to previously set properties.
        """
        distances = []
        if self.types:
            for type_ in metadata1.column_type.keys():
                if metadata1.column_type[type_] == set() or metadata2.column_type[type_] == set():
                    continue
                dist_table = self.__compare_types(type_, metadata1, metadata2)
                if not dist_table.empty:
                    distances.append((self.distance_function.compute(dist_table),
                                  get_ratio(
                                      dist_table.shape[0],
                                      dist_table.shape[1],
                                  ),
                                  self.type_weight))
        if self.kinds:
            for kind in metadata1.column_kind.keys():
                if metadata1.column_kind[kind] != () and  metadata2.column_kind[kind] != ():
                    dist_table = self.__compare_kinds(kind, metadata1, metadata2)
                    if not dist_table.empty:
                        distances.append((self.distance_function.compute(dist_table),
                                      get_ratio(
                                          dist_table.shape[0],
                                          dist_table.shape[1],
                                      ),
                                      self.kind_weight))

        result = 0
        nan = 0
        sum_weight = sum([weight for _,_, weight in distances if not np.isnan(weight)])
        for dist, ratio, weight in distances:
            if math.isnan(dist):
                nan += 1
                continue
            if Settings.NO_RATIO in self.settings:
                result += dist * dist * weight/sum_weight
            else:
                result += dist * dist * ratio * weight/sum_weight
        if nan == len(distances):
            return SimilarityOutput(distance=1)
        return SimilarityOutput(distance=np.sqrt(result))
