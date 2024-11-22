from dataclasses import dataclass
from enum import Enum

from similarity_framework.src.models.metadata import Metadata


@dataclass
class SimilarityConfiguration:
    ...
    # TODO: Thesis add proper fields - I guess this will replace settings


@dataclass
class SimilarityOutput:
    distance: float
    # TODO: Thesis add other proper fields


@dataclass
class SimilarityInput:
    metadata1: Metadata
    metadata2: Metadata

    similarity_configuration: SimilarityConfiguration


class Settings(Enum):
    """Settings enum, if we want to use embeddings for columns, ratio between different comparators"""

    EMBEDDINGS = 1
    NO_RATIO = 2
