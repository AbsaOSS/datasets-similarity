from abc import abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable


class FileType(str, Enum):
    CSV = "csv"
    PARQUET = "parquet"

class ConnectorSettings:
    @staticmethod
    @abstractmethod
    def required_fields() -> list[tuple[str, str]]:
        pass


@dataclass
class FSConnectorSettings(ConnectorSettings):
    """
    ConnectorSettings class is a base class for connector settings.
    """

    filetypes: Iterable[FileType]
    files_paths: list[str] = field(default_factory=lambda: [])
    directory_paths: list[str] = field(default_factory=lambda: [])

    def __init__(self, filetypes: str, files_paths: str, directory_paths: str, **_):
        self.filetypes = [FileType(item) for item in filetypes.split(",")]
        self.files_paths = files_paths.split(",")
        self.directory_paths = directory_paths.split(",")

    @staticmethod
    def required_fields() -> list[tuple[str, str]]:
        return [
            ("filetypes", f"Filetypes to scan for - available: {[item.name.lower() for item in list(FileType)]}, comma separated - csv,json"),
            ("files_paths", "Filepaths to try add for analysis, comma separated - /path/to/file1,/path/to/file2"),
            ("directory_paths", "Directory paths to scan for files, comma separated - /path/to/folder1,/path/to/folder2"),
        ]
