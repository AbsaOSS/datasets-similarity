"""
This module contains the user models
"""
from enum import EnumType

from pydantic import BaseModel

from Comparator import Comparator
from ComparatorByColumn import ComparatorByColumn
from models.connector_models import ConnectorSettings


class SimilarityOutput(BaseModel):
    """
    SimilarityOutput class isclass containing similarity output.
    """

    # here will be common fields for all similarity models
    table_names: list[str]
    distances: dict[(str, str), float]

class MetadataSettings(BaseModel):
    """
    MetadataSettings class is a base class for metadata settings.
    """
    all: bool
    kinds: bool
    types: bool
    embeddings: bool

class RunType(EnumType):
    ALL = "all"
    METADATA = "metadata"
    SIMILARITY = "similarity"

class ComparatorType(EnumType):
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
