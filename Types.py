from enum import Enum


class Types(Enum):
    """
    Enum class representing column type
    """
    NUMERICAL = 1
    INT = 5
    FLOAT = 6
    BOOL = 8
    DATE = 7
    STRING = 3
    TEXT = 4
    UNDEFINED = 0
