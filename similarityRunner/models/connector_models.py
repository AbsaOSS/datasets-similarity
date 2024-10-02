"""
Connector models module contains:
 - the base class for connector settings and derived classes.
 - the base class for connector output and derived classes.
"""
from enum import Enum

import pandas as pd
from pydantic import BaseModel

Output = tuple[list[pd.DataFrame], list[str]]

class FileType(Enum):
    CSV = "csv"
    PARQUET = "parquet"


class ConnectorSettings(BaseModel):
    """
    ConnectorSettings class is a base class for connector settings.
    """

    file_type: tuple[FileType, ...] # csv, parquet, etc., tuple for immutability
    class Config:
        # arbitrary_types_allowed is set to True to allow tuple FileType
        arbitrary_types_allowed = True


class ConnectorOutput(BaseModel):
    """
    ConnectorOutput class is a base class for connector output.
    """
    names: list[str]
    tables: list[pd.DataFrame]

    class Config:
        # arbitrary_types_allowed is set to True to allow list of pandas DataFrames
        arbitrary_types_allowed = True


class FSConnectorSettings(ConnectorSettings):
    """
    FSConnectorSettings class is a derived class for filesystem connector settings.
    """
    files_paths: list[str]
    directory_paths: list[str]

class S3ConnectorSettings(ConnectorSettings):
    """
    S3ConnectorSettings class is a derived class for S3 connector settings.
    """
    pass
