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
"""Authentication utilities for FastAPI application."""

from datetime import datetime, timedelta
from typing import Any, Optional, Coroutine, Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext

from src.main.app.common.config.config_manager import load_config
from src.main.app.common.schema.common_schema import CurrentUser

# Configuration
config = load_config()
security_config = config.security
server_config = config.server

# Security setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{server_config.api_version}/user/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def decode_jwt_token(token: str) -> dict[str, Any]:
    """Decode and validate JWT token.

    Args:
        token: JWT token string

    Returns:
        Decoded token payload

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        return jwt.decode(token, security_config.secret_key, algorithms=[security_config.algorithm])
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token has expired. Please log in again.",
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials.",
        )


def get_current_user() -> Callable[..., Coroutine[Any, Any, CurrentUser]]:
    """Dependency to get current authenticated user.

    Returns:
        Coroutine that resolves to CurrentUser.
        If security is disabled, returns a default user (user_id=0).
    """
    if not security_config.enable:

        async def _default_user() -> CurrentUser:
            return CurrentUser(user_id=0)

        return _default_user

    async def _current_user(token: str = Depends(oauth2_scheme)) -> CurrentUser:
        payload = await decode_jwt_token(token)
        return CurrentUser(user_id=int(payload["sub"]))

    return _current_user


async def create_access_token(
    subject: Optional[str], expires_delta: Optional[timedelta] = None, token_type: Optional[str] = None
) -> str:
    """Create new JWT token.

    Args:
        subject: Token subject (usually user ID)
        expires_delta: Optional timedelta for token expiration
        token_type: Token type identifier

    Returns:
        Encoded JWT string
    """
    expire = datetime.now() + (expires_delta or timedelta(minutes=security_config.refresh_token_expire_minutes))
    to_encode = {"exp": expire, "sub": str(subject), "type": token_type}
    return jwt.encode(to_encode, security_config.secret_key, algorithm=security_config.algorithm)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hashed version.

    Args:
        plain_password: Input password
        hashed_password: Stored hashed password

    Returns:
        True if passwords match
    """
    return pwd_context.verify(plain_password, hashed_password)


async def get_password_hash(password: str) -> str:
    """Generate password hash.

    Args:
        password: Plain text password

    Returns:
        Hashed password string
    """
    return pwd_context.hash(password)


async def validate_token(token: str) -> bool:
    """Check if token is valid and not expired.

    Args:
        token: JWT token to validate

    Returns:
        True if token is valid

    Raises:
        HTTPException: If token is invalid
    """
    try:
        payload = await decode_jwt_token(token)
        if datetime.fromtimestamp(payload["exp"]) < datetime.now():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
        return True
    except JWTError:
        return False
