"""System response code"""

from enum import Enum


class SystemResponseCode(Enum):
    SUCCESS = (0, "Success")
    SERVICE_INTERNAL_ERROR = (-1, "service internal error")

    def __init__(self, code, msg):
        self.code = code
        self.msg = msg
