from enum import Enum

from pydantic import BaseModel

from src.models.metadata import Metadata


class SimilarityConfiguration(BaseModel):
    ...
    # TODO: Thesis add proper fields - I guess this will replace settings


class SimilarityOutput(BaseModel):
    distance: float
    # TODO: Thesis add other proper fields


# class SimilarityInput(BaseModel):
#     metadata1: Metadata
#     metadata2: Metadata
#
#     similarity_configuration: SimilarityConfiguration


# TODO: Thesis These classes should be the once that are provided in the interfaces of Comparators
#   + since they are pydantic models, they will validate inputs, see https://docs.pydantic.dev/latest/concepts/validators/
#   but i think we may drop this technology and invest the time into something 'better'

class Settings(Enum):
    """Settings enum, if we want to use embeddings for columns, ratio between different comparators"""

    EMBEDDINGS = 1
    NO_RATIO = 2