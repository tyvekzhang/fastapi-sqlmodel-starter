"""User domain service impl"""

import http
import io
from datetime import timedelta
from typing import Optional, List

import pandas as pd
from fastapi import UploadFile
from fastapi_pagination import Params
from starlette.responses import StreamingResponse

from fss.common.cache.cache import get_cache_client, Cache
from fss.common.config import configs
from fss.common.enum.enum import TokenTypeEnum
from fss.common.exception.exception import ServiceException
from fss.common.schema.schema import Token
from fss.common.security import security
from fss.common.service.impl.service_impl import ServiceImpl
from fss.common.util.excel import export_template
from fss.common.security.security import verify_password, get_password_hash
from fss.starter.system.enum.system import SystemResponseCode, SystemConstantCode
from fss.starter.system.exception.system import SystemException
from fss.starter.system.mapper.user_mapper import UserMapper
from fss.starter.system.model.user_do import UserDO
from fss.starter.system.schema.user_schema import (
    UserQuery,
    LoginCmd,
    UserExport,
    UserCreateCmd,
)
from fss.starter.system.service.user_service import UserService


class UserServiceImpl(ServiceImpl[UserMapper, UserDO], UserService):
    """
    Implementation of the UserService interface.
    """

    def __init__(self, mapper: UserMapper):
        """
        Initialize the UserServiceImpl instance.

        Args:
            mapper (UserMapper): The UserMapper instance to use for database operations.
        """
        super().__init__(mapper=mapper)
        self.mapper = mapper

    async def find_by_id(self, id: int) -> Optional[UserQuery]:
        """
        Retrieve a user by ID.

        Args:
            id (int): The user ID to retrieve.

        Returns:
            Optional[UserQuery]: The user query object if found, None otherwise.
        """
        user_do = await self.mapper.select_record_by_id(id=id)
        return UserQuery(**user_do.model_dump()) if user_do else None

    async def login(self, loginCmd: LoginCmd) -> Token:
        """
        Perform login and return an access token and refresh token.

        Args:
            loginCmd (LoginCmd): The login command containing username and password.

        Returns:
            Token: The access token and refresh token.
        """
        username: str = loginCmd.username
        userDO: UserDO = await self.mapper.get_user_by_username(username=username)
        if userDO is None or not verify_password(loginCmd.password, userDO.password):
            raise SystemException(
                SystemResponseCode.AUTH_FAILED.code,
                SystemResponseCode.AUTH_FAILED.msg,
                status_code=http.HTTPStatus.UNAUTHORIZED,
            )
        access_token_expires = timedelta(minutes=configs.access_token_expire_minutes)
        access_token = await security.create_token(
            subject=userDO.id,
            expires_delta=access_token_expires,
            token_type=TokenTypeEnum.access,
        )
        refresh_token = await security.create_token(
            subject=userDO.id,
            token_type=TokenTypeEnum.refresh,
        )
        token = Token(
            access_token=access_token,
            expired_at=int(access_token_expires.total_seconds()),
            token_type="bearer",
            refresh_token=refresh_token,
            re_expired_at=int(
                timedelta(minutes=configs.refresh_token_expire_minutes).total_seconds()
            ),
        )
        cache_client: Cache = await get_cache_client()
        await cache_client.set(
            f"{SystemConstantCode.USER_KEY.msg}{userDO.id}",
            access_token,
            access_token_expires,
        )
        return token

    async def export_user_template(
        self,
    ) -> StreamingResponse:
        """
        Export an empty user import template.
        """
        return await export_template(schema=UserExport, file_name="user_template")

    async def import_user(self, file: UploadFile):
        """
        Import user record from an Excel file.

        Args:
            file (UploadFile): The Excel file containing user record.
        """
        contents = await file.read()
        import_df = pd.read_excel(io.BytesIO(contents))
        user_records: UserQuery = [
            user_record for user_record in import_df.to_dict(orient="records")
        ]
        user_import_list = []
        user_name_list = []
        for user_record in user_records:
            user_import = UserDO(**user_record)
            user_import.password = await get_password_hash(user_import.password)
            user_import_list.append(user_import)
            user_name_list.append(user_import.username)
        await file.close()
        user_list: List[UserDO] = await self.mapper.get_user_by_usernames(
            usernames=user_name_list
        )

        if len(user_list) > 0:
            err_msg = ""
            for user in user_list:
                err_msg += "," + str(user.username)
            raise SystemException(
                SystemResponseCode.USER_NAME_EXISTS.code,
                SystemResponseCode.USER_NAME_EXISTS.msg + err_msg,
            )
        await self.mapper.batch_insert_records(records=user_import_list)

    async def export_user(self, params: Params) -> StreamingResponse:
        """
        Export user record to an Excel file.

        Args:
            params (Params): The query parameters for filtering users.

        Returns:
            StreamingResponse: The Excel file containing user record.
        """
        user_pages, _ = await self.mapper.select_records(
            page=params.page, size=params.size
        )
        records = []
        for user in user_pages:
            records.append(UserQuery(**user.model_dump()))
        return await export_template(
            schema=UserQuery, file_name="user", records=records
        )

    async def register(self, record: UserCreateCmd) -> UserDO:
        """
        Register a new user.

        Args:
            record (UserCreateCmd): The user creation command containing username and password.

        Returns:
            UserDO: The newly created user.
        """
        record.password = await get_password_hash(record.password)
        user: UserDO = await self.mapper.get_user_by_username(username=record.username)
        if user is not None:
            raise ServiceException(
                SystemResponseCode.USER_NAME_EXISTS.code,
                SystemResponseCode.USER_NAME_EXISTS.msg,
            )
        return await self.mapper.insert_record(record=record)

    async def retrieve_user(self, page: int, size: int) -> Optional[List[UserQuery]]:
        """
        List users with pagination.

        Args:
            page (int): The page number.
            size (int): The page size.

        Returns:
            Optional[List[UserQuery]]: The list of users or None if no users are found.
        """
        results, _ = await self.mapper.select_records(page=page, size=size)
        return [UserQuery(**user.model_dump()) for user in results]
