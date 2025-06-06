"""User domain service impl"""

import http
import io
from datetime import timedelta
from typing import Optional, List

import pandas as pd
from fastapi import UploadFile
from fastapi_pagination import Params
from starlette.responses import StreamingResponse

from src.main.app.common.cache import base_cache, cache_manager
from src.main.app.common.config.config_manager import load_config
from src.main.app.common.enums.common_enum import TokenTypeEnum
from src.main.app.common.schema.common_schema import Token
from src.main.app.common.security import common_security
from src.main.app.common.security.common_security import verify_password, get_password_hash
from src.main.app.common.service.impl.base_service_impl import BaseServiceImpl
from src.main.app.common.utils.excel_util import export_template
from src.main.app.entity.user_entity import UserEntity
from src.main.app.enums.biz_error_code import BusinessErrorCode
from src.main.app.enums.enum import SystemResponseCode
from src.main.app.exception import biz_exception
from src.main.app.exception.biz_exception import BusinessException
from src.main.app.mapper.user_mapper import UserMapper
from src.main.app.schema.user_schema import (
    UserQuery,
    LoginForm,
    UserExport,
    UserCreate,
)
from src.main.app.service.user_service import UserService


class UserServiceImpl(BaseServiceImpl[UserMapper, UserEntity], UserService):
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
        user_entity = await self.mapper.select_by_id(id=id)
        return UserQuery(**user_entity.model_dump()) if user_entity else None

    async def login(self, login_form: LoginForm) -> Token:
        """
        Perform login and return an access token and refresh token.

        Args:
            login_form (LoginForm): The login command containing username and password.

        Returns:
            Token: The access token and refresh token.
        """
        # verify username and password
        username: str = login_form.username
        user_entity: UserEntity = await self.mapper.get_user_by_username(username=username)
        if user_entity is None or not verify_password(login_form.password, user_entity.password):
            raise biz_exception.BusinessException(
                SystemResponseCode.AUTH_FAILED.code,
                SystemResponseCode.AUTH_FAILED.msg,
                status_code=http.HTTPStatus.UNAUTHORIZED,
            )
        # generate access token
        security_config = load_config().security
        access_token_expires = timedelta(minutes=security_config.access_token_expire_minutes)
        access_token = await security.create_token(
            subject=user_entity.id,
            expires_delta=access_token_expires,
            token_type=TokenTypeEnum.access,
        )
        # generate refresh token
        refresh_token = await security.create_token(
            subject=user_entity.id,
            token_type=TokenTypeEnum.refresh,
        )
        token = Token(
            access_token=access_token,
            expired_at=int(access_token_expires.total_seconds()),
            token_type=TokenTypeEnum.bearer,
            refresh_token=refresh_token,
            re_expired_at=int(timedelta(minutes=security_config.refresh_token_expire_minutes).total_seconds()),
        )
        # cache token info
        cache_client: base_cache.Cache = await cache_manager.get_cache_client()
        await cache_client.set(
            f"User:{user_entity.id}",
            access_token,
            access_token_expires,
        )
        return token

    async def export_user_template(self, file_name: str = "user_template") -> StreamingResponse:
        """
        Export an empty user import template.

        Args:
            file_name: File name for export
        """
        return await export_template(schema=UserExport, file_name=file_name)

    async def import_user(self, file: UploadFile):
        """
        Import user record from an Excel file.

        Args:
            file (UploadFile): The Excel file containing user record.
        """
        contents = await file.read()
        import_df = pd.read_excel(io.BytesIO(contents))
        user_records = import_df.to_dict(orient="records")
        if len(user_records) == 0:
            return

        user_import_list = []
        user_name_list = []

        for user_record in user_records:
            user_import = UserEntity(**user_record)
            user_import.password = await get_password_hash(user_import.password)
            user_import_list.append(user_import)
            user_name_list.append(user_import.username)
        await file.close()

        # Check if any usernames already exist
        existing_users: List[UserEntity] = await self.mapper.get_user_by_usernames(usernames=user_name_list)

        if existing_users:
            existing_usernames = [user.username for user in existing_users]
            err_msg = ",".join(existing_usernames)
            raise BusinessException(
                BusinessErrorCode.USER_NAME_EXISTS,
                f"{BusinessErrorCode.USER_NAME_EXISTS.msg}{err_msg}",
            )
        await self.mapper.batch_insert(records=user_import_list)

    async def export_user(self, params: Params, file_name: str = "user") -> StreamingResponse:
        """
        Export user record to an Excel file.

        Args:
            params (Params): The query parameters for filtering users.
            file_name: File name for export

        Returns:
            StreamingResponse: The Excel file containing user record.
        """
        user_pages, _ = await self.mapper.select_by_page(page=params.page, size=params.size)
        records = []
        for user in user_pages:
            records.append(UserQuery(**user.model_dump()))
        return await export_template(schema=UserQuery, file_name=file_name, records=records)

    async def register(self, user_create: UserCreate) -> UserEntity:
        """
        Register a new user.

        Args:
            user_create (UserCreate): The user creation command containing username and password.

        Returns:
            UserEntity: The newly created user.
        """
        # user name duplicate verification
        user: UserEntity = await self.mapper.get_user_by_username(username=user_create.username)
        if user is not None:
            raise BusinessException(BusinessErrorCode.USER_NAME_EXISTS)
        # generate hash password
        user_create.password = await get_password_hash(user_create.password)
        return await self.mapper.insert(record=user_create)

    async def retrieve_user(self, page: int, size: int, **kwargs) -> Optional[List[UserQuery]]:
        """
        List users with pagination.

        Args:
            page (int): The page number.
            size (int): The page size.

        Returns:
            Optional[List[UserQuery]]: The list of users or None if no users are found.
        """
        results, _ = await self.mapper.select_by_page(page=page, size=size, **kwargs)
        return [UserQuery(**user.model_dump()) for user in results]
