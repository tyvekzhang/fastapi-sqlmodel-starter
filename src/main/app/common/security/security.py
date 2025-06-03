"""Open OAuth2PasswordBearer and provide current user info"""

import http
from datetime import timedelta, datetime
from typing import Any, Union, Callable, Coroutine

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError
from jose import jwt
from multipart.exceptions import DecodeError
from passlib.context import CryptContext
from starlette import status
from starlette.responses import JSONResponse

from src.main.app.common.config.config_manager import load_config

from src.main.app.common.schema.schema import CurrentUser

security_config = load_config().security
server_config = load_config().server
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{server_config.api_version}/user/login")


def get_current_user() -> Callable[[str], Coroutine[Any, Any, CurrentUser]]:
    """
    Acquire current info through access_token
    :return: CurrentUser instance
    """

    async def current_user(
        access_token: str = Depends(oauth2_scheme),
    ) -> CurrentUser:
        try:
            payload = await get_payload(access_token)
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
        user_id = payload["sub"]

        return CurrentUser(user_id=user_id)

    return current_user


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_token(subject: Union[str, Any], expires_delta: timedelta = None, token_type: str = None) -> str:
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=security_config.refresh_token_expire_minutes)
    to_encode = {"exp": expire, "sub": str(subject), "type": token_type}
    encoded_jwt = jwt.encode(to_encode, security_config.secret_key, algorithm=security_config.algorithm)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    match: bool = pwd_context.verify(plain_password, hashed_password)
    return match


async def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def get_payload(token: str):
    return jwt.decode(token, security_config.secret_key, algorithms=security_config.algorithm)


def get_user_id(token: str):
    payload = jwt.decode(token, security_config.secret_key, algorithms=security_config.algorithm)
    return payload["sub"]


async def is_valid_token(token: str):
    payload = await get_payload(token)
    exp = payload.get("exp")
    now = datetime.now()
    if exp and datetime.fromtimestamp(exp) < now:
        return JSONResponse(
            status_code=http.HTTPStatus.UNAUTHORIZED,
            content={"detail": "Token has expired"},
        )
