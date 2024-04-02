"""Security util, such as encode decode and etc"""

from datetime import timedelta, datetime
from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext
from redis.asyncio import Redis

from fss.common.config import configs

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"
DAYS_WITHOUT_LOGIN = 30


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(days=DAYS_WITHOUT_LOGIN)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, configs.secret_key, algorithm=ALGORITHM)
    return encoded_jwt


async def add_token_to_redis(
    redis_client: Redis, user_id: int, access_token: str, ex: int
):
    token_key = f"user:{user_id}"
    await redis_client.set(token_key, access_token, ex=ex)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
