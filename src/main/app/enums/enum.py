# Copyright (c) 2025 Fast web and/or its affiliates. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""System response code"""

from enum import Enum

from src.main.app.common.enums.base_error_code import BaseErrorCode


class SystemErrorEnum(BaseErrorCode):
    """System and infrastructure related errors"""

    INTERNAL_ERROR = (500, "Internal server error")
    SERVICE_UNAVAILABLE = (503, "Service unavailable")
    DATABASE_ERROR = (5001, "Database operation failed")


class SystemResponseCode(Enum):
    """
    Enum for system response codes.
    """

    def __init__(self, code, msg):
        """
        Initialize a system response code.

        Args:
            code (int): The response code.
            msg (str): The response message.
        """
        self.code = code
        self.msg = msg

    SUCCESS = (0, "Success")
    SERVICE_INTERNAL_ERROR = (-1, "Service internal error")

    PARAMETER_ERROR = (400, "Parameter error")
    AUTH_FAILED = (401, "Username or password error")
    PARAMETER_CHECK_ERROR = (402, "Parameter error")
    DELETE_PARAMETER_ERROR = (403, "Delete parameter error")

    ROLE_ALREADY_EXISTS = (101, "Assign role already exists")


class SystemConstantCode(Enum):
    """
    Enum for system constant codes.
    """

    def __init__(self, code, msg):
        """
        Initialize a system constant code.

        Args:
            code (int): The constant code.
            msg (str): The constant message.
        """
        self.code = code
        self.msg = msg

    USER_KEY = (10, "user:")
