# -*- coding: utf-8 -*-
# Copyright (c) 2025 Fast web
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

"""System-related error codes (10000-19999)."""

from src.main.app.common.enums.base_error_code import CustomExceptionCode


class SystemErrorCode(CustomExceptionCode):
    """System-related error codes."""

    INTERNAL_ERROR = (10001, "Internal server error")
    SERVICE_UNAVAILABLE = (10002, "Service temporarily unavailable")
    DATABASE_ERROR = (10003, "Database operation failed")
    CONFIGURATION_ERROR = (10004, "System configuration error")
    FILE_OPERATION_ERROR = (10005, "File operation failed")
    NETWORK_ERROR = (10006, "Network communication error")
    EXTERNAL_SERVICE_ERROR = (10007, "External service error")
    RESOURCE_EXHAUSTED = (10008, "Resource exhausted")
    TIMEOUT_ERROR = (10009, "Operation timed out")
