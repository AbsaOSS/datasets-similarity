from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Iterable


class ConnectorSettings:
    pass

class FileType(str, Enum):
    CSV = "csv"
    PARQUET = "parquet"

@dataclass
class FSConnectorSettings(ConnectorSettings):
    """
    ConnectorSettings class is a base class for connector settings.
    """
    filetypes: Iterable[FileType]
    files_paths: list[str] = field(default_factory=lambda: list())
    directory_paths: list[str] = field(default_factory=lambda: list())
