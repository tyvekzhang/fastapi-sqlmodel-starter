from typing import Callable

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError
from multipart.exceptions import DecodeError
from starlette import status

from fss.common.config import configs
from fss.common.schema.schema import CurrentUser
from fss.common.util.security import get_payload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{configs.api_version}/user/login")


def get_current_user() -> Callable[[], CurrentUser]:
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
