"""System response code"""

from enum import Enum


class SystemResponseCode(Enum):
    SUCCESS = (0, "Success")
    SERVICE_INTERNAL_ERROR = (-1, "service internal error")
    AUTH_FAILED = (401, "service internal error")
    PARAMETER_ERROR = (400, "parameter_error")

    def __init__(self, code, msg):
        self.code = code
        self.msg = msg


class SystemConstantCode(Enum):
    USER_KEY = (10, "user:")

    def __init__(self, code, msg):
        self.code = code
        self.msg = msg
