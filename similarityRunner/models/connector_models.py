"""
Connector models module contains:
 - the base class for connector settings and derived classes.
 - the base class for connector output and derived classes.
"""
from enum import Enum

import pandas as pd
from pydantic import BaseModel

Output = pd.DataFrame

class FileType(Enum):
    CSV = "csv"
    PARQUET = "parquet"


class ConnectorSettings(BaseModel):
    """
    ConnectorSettings class is a base class for connector settings.
    """

    # here will be common fields for all connectors
    file_type: tuple[FileType] # csv, parquet, etc., tuple for immutability


class ConnectorOutput(BaseModel):
    """
    ConnectorOutput class is a base class for connector output.
    """
    names: list[str]
    tables: tuple[list[pd.DataFrame]]
    # here will be common fields for all connectors

class FSConnectorSettings(ConnectorSettings):
    """
    FSConnectorSettings class is a derived class for filesystem connector settings.
    """
    files_paths: list[str]
    directory_paths: list[str]
