"""Common enumerations"""

from enum import Enum


class ModeEnum(str, Enum):
    """
    Enum for specifying the mode of operation.
    """

    development = "dev"
    production = "prod"
    testing = "test"


class SortEnum(str, Enum):
    """
    Enum for specifying sorting order.
    """

    ascending = "asc"
    descending = "desc"


class TokenTypeEnum(str, Enum):
    """
    Enum for token type.
    """

    access = "access"
    refresh = "refresh"
