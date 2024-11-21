from abc import abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable


class ConnectorSettings:
    @staticmethod
    @abstractmethod
    def required_fields() -> list[tuple[str, str]]:
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

    @staticmethod
    def required_fields() -> list[tuple[str, str]]:
        return [
            ("filetypes", "Filetypes to scan for"),
            ("files_paths", "Filepaths to try add for analysis"),
            ("directory_paths", "Diredtory paths to scan for files"),
        ]