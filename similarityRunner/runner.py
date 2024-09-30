"""
This
"""

from Comparator import Comparator
from ComparatorByColumn import ComparatorByColumn, ColumnKindComparator, ColumnExactNamesComparator
from DataFrameMetadata import DataFrameMetadata
from DataFrameMetadataCreator import DataFrameMetadataCreator
from connectors.filesystem_connector import FilesystemConnector
from interfaces.OutputFormaterInterface import OutputFormaterInterface
from models.connector_models import Output
from models.user_models import SimilaritySettings

def create_metadata(settings: SimilaritySettings, data: Output) -> dict[str, DataFrameMetadata]:
    """
    Create metadata for each table in the data
    """
    dataframes, names = data
    df_metadata = {}
    if settings.metadata.all:
        for df, name in zip(dataframes, names):
            df_metadata[name] = (DataFrameMetadataCreator(df)
                                 .create_column_embeddings()
                                 .compute_advanced_structural_types()
                                 .compute_column_kind()
                                 .get_metadata())
    else:
        ... # todo after #35

    # todo save metadata after #35
    return df_metadata


def __get_comparator(settings: SimilaritySettings):
    """
    Get comparator based on settings
    """
    if settings.comparator_type == "BY_COLUMN":
        comp = ComparatorByColumn()
        return comp.add_comparator_type(ColumnKindComparator()).add_comparator_type(ColumnExactNamesComparator())
        # todo add by settings #35
    return Comparator() # todo #35

def compute_similarity(settings: SimilaritySettings, data: dict[str, DataFrameMetadata]):
    """
    Compute similarity between tables
    """
    comparator = __get_comparator(settings)
    similarity = {}
    for name, met in data.items():
        for name2, met2 in data.items():
            similarity[(name, name2)] = comparator.compare(met, met2)
    return similarity

def run(settings: SimilaritySettings):
    """
    Run the similarity pipeline
    """
    data = FilesystemConnector().get_data(settings.connector)
    if settings.run_type == "all":
        print("Creating metadata ...")
        met = create_metadata(settings, data)
        print("Metadata created")
        print("Computing similarity ...")
        res = compute_similarity(settings, met)
        return OutputFormaterInterface().format_output(res)
    elif settings.run_type == "metadata":
        create_metadata(settings, data)
    elif settings.run_type == "similarity":
        print("Similarity") # todo after #35
