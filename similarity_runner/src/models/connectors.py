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

    @staticmethod
    @abstractmethod
    def optional_fields() -> list[tuple[str, str]]:
        pass

