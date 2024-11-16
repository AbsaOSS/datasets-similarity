from enum import Enum

from pydantic import BaseModel


class SimilarityOutput(BaseModel):
    ...


class SimilarityInput(BaseModel):
    ...


class SimilarityConfiguration(BaseModel):
    ...


class Settings(Enum):
    """Settings enum, if we want to use embeddings for columns, ratio between different comparators"""

    EMBEDDINGS = 1
    NO_RATIO = 2