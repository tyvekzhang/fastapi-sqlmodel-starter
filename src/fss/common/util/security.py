"""Security util, such as encode decode and etc"""

from datetime import timedelta, datetime
from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext
from starlette.responses import JSONResponse

from fss.common.config import configs

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
DAYS_WITHOUT_LOGIN = 30


async def create_token(
    subject: Union[str, Any], expires_delta: timedelta = None, token_type: str = None
) -> str:
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(days=DAYS_WITHOUT_LOGIN)
    to_encode = {"exp": expire, "sub": str(subject), "type": token_type}
    encoded_jwt = jwt.encode(to_encode, configs.secret_key, algorithm=configs.algorithm)
    return encoded_jwt


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    match: bool = pwd_context.verify(plain_password, hashed_password)
    return match


async def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def get_payload(token: str):
    return jwt.decode(token, configs.secret_key, algorithms=configs.algorithm)


def get_user_id(token: str):
    payload = jwt.decode(token, configs.secret_key, algorithms=configs.algorithm)
    return payload["sub"]


async def is_valid_token(token: str):
    payload = await get_payload(token)
    exp = payload.get("exp")
    now = datetime.now()
    if exp and datetime.fromtimestamp(exp) < now:
        return JSONResponse(
            status_code=401,
            content={"detail": "Token has expired"},
        )
