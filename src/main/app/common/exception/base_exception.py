# -*- coding: utf-8 -*-
# Copyright 2025 Fast web
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
"""Base exception classes for the application."""

from typing import Optional, Any

from src.main.app.common.exception.base_error_code import BaseErrorCode


class BaseError(Exception):
    """Base exception class for all custom exceptions in the application.

    Attributes:
        error_code: The error code enum member from BaseErrorCode or its subclasses.
        message: Optional custom message that overrides the default error message.
        details: Optional additional details about the error.
    """

    def __init__(
            self,
            error_code: BaseErrorCode,
            message: Optional[str] = None,
            details: Optional[Any] = None,
    ):
        """
        Args:
            error_code: An enum member from BaseErrorCode or its subclasses.
            message: Optional custom message to override the default error message.
            details: Optional additional details about the error.
        """
        self.error_code = error_code
        self.message = message or error_code.msg
        self.details = details
        super().__init__(self.message)

    def __str__(self) -> str:
        """Returns string representation of the error."""
        if self.details:
            return f"{self.error_code.code}: {self.message} (Details: {self.details})"
        return f"{self.error_code.code}: {self.message}"

    def to_dict(self) -> dict:
        """Converts the exception to a dictionary for API responses.

        Returns:
            A dictionary containing error code, message, and details (if any).
        """
        result = {
            "error_code": self.error_code.code,
            "message": self.message,
        }
        if self.details:
            result["details"] = self.details
        return result