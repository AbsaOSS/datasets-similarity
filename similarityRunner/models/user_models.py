"""
This module contains the user models
"""
from pydantic import BaseModel


class SimilarityOutput(BaseModel):
    """
    SimilarityOutput class isclass containing similarity output.
    """
    # here will be common fields for all similarity models
    table_names: list[str]
    distances: dict[(str, str),float]
