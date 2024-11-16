"""
This files contains all types and kinds
"""

import re
from enum import Enum



class DataKind(Enum):
    """
    Represents all data kind.
    """

    BOOL = "bool"
    ID = "id"
    CONSTANT = "constant"
    UNDEFINED = "undefined"
    CATEGORICAL = "categorical"

class Type:
    """
    Base class for type
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return ""


class DATE(Type):
    """
    Represents type date.
    """

    def __str__(self):
        return "DATE"


class UNDEFINED(Type):
    """
    Represents class undefined
    """

    def __str__(self):
        return "UNDEFINED"


class NUMERICAL(Type):
    """
    Represents numerical types.
    """

    def __str__(self):
        return "NUMERICAL"


class INT(NUMERICAL):
    """
    Represents INT type.
    """

    def __str__(self):
        return "INT"


class FLOAT(NUMERICAL):
    """
    Represents FLOAT type.
    """

    def __str__(self):
        return "FLOAT"


class HUMAN_GENERATED(FLOAT):
    """
    Represents float, which is probably generated by human.
    Number of numbers after floating point is small or rounded.
    """

    def __str__(self):
        return "HUMAN_GENERATED"


class COMPUTER_GENERATED(FLOAT):
    """
    Represents float, which is probably generated by computer.
    Number of numbers after floating point is bigger or not rounded.
    """

    def __str__(self):
        return "COMPUTER_GENERATED"


class NONNUMERICAL(Type):
    """
    Subclass for nonnumerical types
    """

    def __str__(self):
        return "NONNUMERICAL"


class WORD(NONNUMERICAL):
    """
    Word is string without spaces.
    """

    def __str__(self):
        return "WORD"


class ALPHABETIC(WORD):
    """
    This type is WORD, it contains only letters (a-z)
    """

    def __str__(self):
        return "ALPHABETIC"


class ALPHANUMERIC(WORD):
    """
    This type is WORD, it contains only letters (a-z) and numbers (0-9)
    """

    def __str__(self):
        return "ALPHANUMERIC"


class ALL(WORD):
    """
    This type is WORD, it could contain all characters.
    """

    def __str__(self):
        return "ALL"


class SENTENCE(NONNUMERICAL):
    """
    Sentence is string that ends with fullstops. It could contain spaces.
    """

    def __str__(self):
        return "SENTENCE"


class ARTICLE(NONNUMERICAL):
    """
    Article is string composite from sentences.
    """

    def __str__(self):
        return "ARTICLE"


class PHRASE(NONNUMERICAL):
    """
    Phrase is string with spaces, but it is not sentence.
    """

    def __str__(self):
        return "PHRASE"


class MULTIPLE_VALUES(NONNUMERICAL):
    """
    MULTIPLE_VALUES is string, and it contains pattern that is repeated. (Name1|Name2|Name3|Name4)
    """

    def __str__(self):
        return "MULTIPLE_VALUES"
