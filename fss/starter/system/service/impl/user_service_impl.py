"""User domain service impl"""

from datetime import timedelta
from typing import Optional

from fss.common.cache.cache import get_cache_client, Cache
from fss.common.config import configs
from fss.common.enum.enum import TokenTypeEnum
from fss.common.schema.schema import Token
from fss.common.service.impl.service_impl import ServiceImpl
from fss.common.util import security
from fss.common.util.security import verify_password
from fss.starter.system.enum.system import SystemResponseCode, SystemConstantCode
from fss.starter.system.exception.system import SystemException
from fss.starter.system.mapper.user_mapper import UserMapper
from fss.starter.system.model.user_do import UserDO
from fss.starter.system.schema.user_schema import UserQuery, LoginCmd
from fss.starter.system.service.user_service import UserService


class UserServiceImpl(ServiceImpl[UserMapper, UserDO], UserService):
    def __init__(self, mapper: UserMapper):
        super().__init__(mapper)

    async def find_by_id(self, id: int) -> Optional[UserQuery]:
        """
        Retrieval user through user id
        :param id: user id
        :return: user or none
        """
        user_do = await self.mapper.select_by_id(id=id)
        if user_do:
            return UserQuery(**user_do.model_dump())
        else:
            return None

    async def login(self, loginCmd: LoginCmd) -> Token:
        """
        Do log in
        :param loginCmd: loginCmd
        :return: access token and refresh token
        """
        username: str = loginCmd.username
        userDO: UserDO = await self.mapper.get_user_by_username(username=username)
        if not userDO or not await verify_password(loginCmd.password, userDO.password):
            raise SystemException(
                SystemResponseCode.AUTH_FAILED.code, SystemResponseCode.AUTH_FAILED.msg
            )
        access_token_expires = timedelta(minutes=configs.access_token_expire_minutes)
        refresh_token_expires = timedelta(minutes=configs.refresh_token_expire_minutes)
        access_token = await security.create_token(
            subject=userDO.id,
            expires_delta=access_token_expires,
            token_type=TokenTypeEnum.access,
        )
        refresh_token = await security.create_token(
            subject=userDO.id,
            expires_delta=refresh_token_expires,
            token_type=TokenTypeEnum.refresh,
        )
        token = Token(
            access_token=access_token,
            expired_at=int(access_token_expires.total_seconds()),
            token_type="bearer",
            refresh_token=refresh_token,
            re_expired_at=int(refresh_token_expires.total_seconds()),
        )
        cache_client: Cache = await get_cache_client()
        await cache_client.set(
            f"{SystemConstantCode.USER_KEY.msg}{userDO.id}",
            access_token,
            access_token_expires,
        )
        return token


def get_user_service() -> UserService:
    return UserServiceImpl(UserMapper(UserDO))
