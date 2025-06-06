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
"""Open OAuth2PasswordBearer and provide current user info"""

from datetime import timedelta, datetime
from typing import Any, Union, Callable

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError
import jwt
from multipart.exceptions import DecodeError
from passlib.context import CryptContext
from starlette import status

from src.main.app.common.config.config_manager import load_config
from src.main.app.common.schema.common_schema import CurrentUser

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def decode_token(token: str):
    config = load_config()
    """Decode JWT and return payload"""
    key = config.security.secret_key
    return jwt.decode(token, key, algorithms=[config.security.algorithm])


def get_user_id(token: str) -> int:
    """Extract user ID from token"""
    payload = decode_token(token)
    return payload["sub"]


def get_oauth2_scheme() -> OAuth2PasswordBearer:
    config = load_config()
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{config.server.api_version}/user/login")
    return oauth2_scheme


def get_current_user() -> Callable[[], CurrentUser]:
    """
    Acquire current info through access_token

    Returns:
        CurrentUser instance
    """

    def current_user(
        access_token: str = Depends(get_oauth2_scheme()),
    ) -> CurrentUser:
        security = load_config().security
        if not security.enable:
            user_id = 1
            return CurrentUser(id=user_id)
        try:
            user_id = get_user_id(access_token)
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your token has expired. Please log in again.",
            )
        except DecodeError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Error when decoding the token. Please check your request.",
            )

        return CurrentUser(id=user_id)

    return current_user


def create_token(
    subject: Union[str, Any],
    expires_delta: Union[timedelta, None] = None,
    token_type: str = None,
) -> str:
    """Create a JWT token"""
    config = load_config()
    expire = int(
        (datetime.now() + (expires_delta or timedelta(minutes=config.security.access_token_expire_minutes))).timestamp()
    )
    to_encode = {"exp": expire, "sub": str(subject), "entity": token_type}
    return jwt.encode(to_encode, config.security.secret_key, algorithm=config.security.algorithm)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def get_payload(token: str):
    """Get payload from token"""
    config = load_config()
    return jwt.decode(token, config.security.secret_key, algorithms=config.security.algorithm)


def is_token_valid(token: str) -> bool:
    """Check if the token is valid"""
    try:
        payload = decode_token(token)
        exp = payload.get("exp")
        exp_date = datetime.fromtimestamp(exp)
        now = datetime.now()
        return exp and exp_date > now
    except (ExpiredSignatureError, DecodeError):
        return False
