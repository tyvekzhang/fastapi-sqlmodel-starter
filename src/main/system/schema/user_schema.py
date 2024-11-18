"""User domain schema"""

import re
from typing import Optional, Dict, Any

from pydantic import BaseModel, field_validator
from sqlmodel import Field

from src.common.schema.schema import BasePage


class UserCreateCmd(BaseModel):
    """
    UserCreate schema
    """

    username: str = Field(..., min_length=2, max_length=32)
    password: str = Field(..., min_length=6, max_length=64)
    nickname: str = Field(..., min_length=2, max_length=32)

    @field_validator("password")
    def password_complexity(cls, value):
        """
        Validate password strength:
        - Contains an uppercase letter
        - Contains a lowercase letter
        - Contains a digit
        """
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit")
        return value


class UserQuery(BaseModel):
    """
    UserQuery schema
    """

    id: int
    username: str
    nickname: str


class LoginCmd(BaseModel):
    """
    Login schema
    """

    username: str
    password: str


class UpdateUserCmd(BaseModel):
    """
    Update user schema
    """

    id: int
    nickname: str


class UserExport(BaseModel):
    """
    UserExport schema
    """

    username: str
    password: str
    nickname: str


class UserFilterParams(BasePage):
    """
    UserFilterParams schema
    """

    filter_by: Optional[Dict[str, Any]] = None
    like: Optional[Dict[str, str]] = None
