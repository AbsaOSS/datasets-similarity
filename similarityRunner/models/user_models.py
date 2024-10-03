"""
This module contains the user models
"""

from enum import Enum

from pydantic import BaseModel

from Comparator import Comparator
from ComparatorByColumn import ComparatorByColumn
from models.connector_models import ConnectorSettings


class SimilarityOutput(BaseModel):
    """
    SimilarityOutput class is class containing similarity output.
    """

    # here will be common fields for all similarity models
    table_names: list[str]
    distances: dict[(str, str), float]

    class Config:
        # arbitrary_types_allowed is set to True to allow list and dictionary
        arbitrary_types_allowed = True


class MetadataSettings(BaseModel):
    """
    MetadataSettings class is a base class for metadata settings.
    """

    all: bool
    kinds: bool
    types: bool
    embeddings: bool


class RunType(str, Enum):
    """enum class, which contains run types for which part of the pipeline we would like to run"""
    ALL = "all"
    METADATA = "metadata"
    SIMILARITY = "similarity"


class ComparatorType(Enum):
    """Enum class for comparator types"""
    BY_COLUMN = ComparatorByColumn()
    BY_TYPE = Comparator()


class SimilaritySettings(BaseModel):
    """
    SimilaritySettings class is a base class for similarity settings.
    """

    connector: ConnectorSettings
    metadata: MetadataSettings
    run_type: RunType
    comparator_type: ComparatorType

    class Config:
        # arbitrary_types_allowed is set to True to allow Enum Types
        arbitrary_types_allowed = True
