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

"""Business-related error codes (30000-39999)."""
from src.main.app.common.enums.base_error_code import BaseErrorCode


class BusinessErrorCode(BaseErrorCode):
    """Business-related error codes."""

    USER_NAME_EXISTS = (30001, "Username already exists")

    VALIDATION_ERROR = (30001, "Validation error")
    INVALID_PARAMETER = (30002, "Invalid parameter")
    MISSING_PARAMETER = (30003, "Missing required parameter")
    DUPLICATE_ENTRY = (30004, "Duplicate entry")
    RESOURCE_NOT_FOUND = (30005, "Resource not found")
    OPERATION_NOT_ALLOWED = (30006, "Operation not allowed")
    QUOTA_EXCEEDED = (30007, "Quota exceeded")
    INVALID_STATE = (30008, "Invalid state")
    UNSUPPORTED_OPERATION = (30009, "Unsupported operation")
    BUSINESS_RULE_VIOLATION = (30010, "Business rule violation")
    DATA_INTEGRITY_ERROR = (30011, "Data integrity error")
    LIMIT_EXCEEDED = (30012, "Limit exceeded")
    CONFLICT = (30013, "Conflict detected")
    PRECONDITION_FAILED = (30014, "Precondition failed")