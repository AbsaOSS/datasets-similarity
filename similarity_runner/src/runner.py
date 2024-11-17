"""
This file contains a runner function that can run the pipeline according to settings
"""

import time

from Comparator import Comparator, KindComparator, ColumnExactNamesComparator as ExactNames
from ComparatorByColumn import ComparatorByColumn, ColumnKindComparator, ColumnExactNamesComparator
from DataFrameMetadata import DataFrameMetadata
from DataFrameMetadataCreator import DataFrameMetadataCreator
from src.connectors.filesystem_connector import FilesystemConnector
from src.formators import JsonFormater
from src.models import Output
from src.models import SimilaritySettings, ComparatorType


def create_metadata(settings: SimilaritySettings, data: Output) -> dict[str, DataFrameMetadata]:
    """
    Create metadata for each table in the data
    :param settings: settings for the metadata creation
    :param data: data to create metadata from
    :return: dictionary of metadata for each table
    """
    dataframes, names = data
    df_metadata = {}
    if settings.metadata.all:
        for df, name in zip(dataframes, names):
            df_metadata[name] = DataFrameMetadataCreator(df).create_column_embeddings().compute_advanced_structural_types().compute_column_kind().get_metadata()
    else:
        ...  # todo after #35

    # todo save metadata after #35
    return df_metadata


def __get_comparator(settings: SimilaritySettings):
    """
    Get comparator based on settings
    """
    if settings.comparator_type == ComparatorType.BY_COLUMN:
        comp = ComparatorByColumn()
        return comp.add_comparator_type(ColumnKindComparator()).add_comparator_type(ColumnExactNamesComparator())
        # todo add by settings #35
    comp = Comparator()  # todo add by settings #35
    return comp.add_comparator_type(KindComparator()).add_comparator_type(ExactNames())


def compute_similarity(settings: SimilaritySettings, data: dict[str, DataFrameMetadata]) -> dict[str, dict[str, float]]:
    """
    Compute similarity between tables
    :param settings: settings for the similarity computation
    :param data: metadata of the tables
    """
    comparator = __get_comparator(settings)
    names = list(data.keys())
    similarity = {name: {name2: comparator.compare(data[name], data[name2]) for name2 in names} for name in names}
    return similarity


def run(settings: SimilaritySettings):
    """
    Run the similarity pipeline
    """
    data = FilesystemConnector().get_data(settings.connector)
    if settings.run_type == "all":
        start = time.time()
        print("Creating metadata ...")
        met = create_metadata(settings, data)
        end = time.time()
        print("Metadata created in", end - start, "s")
        print("Computing similarity ...")
        start = time.time()
        res = compute_similarity(settings, met)
        end = time.time()
        print("Similarity computed in", end - start, "s")
        return JsonFormater().format(res)
    elif settings.run_type == "metadata":
        create_metadata(settings, data)
    elif settings.run_type == "similarity":
        print("Similarity")  # todo after #35
