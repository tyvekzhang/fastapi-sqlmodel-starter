"""User domain service interface"""

from abc import ABC, abstractmethod
from typing import Optional, List

from fastapi import UploadFile
from fastapi_pagination import Params
from starlette.responses import StreamingResponse

from src.main.app.common.schema.schema import Token
from src.main.app.common.service.base_service import BaseService
from src.main.app.entity.user_entity import UserEntity
from src.main.app.schema.user_schema import UserQuery, LoginForm, UserCreate


class UserService(BaseService[UserEntity], ABC):
    @abstractmethod
    async def register(self, *, user_create: UserCreate) -> UserEntity: ...

    @abstractmethod
    async def login(self, *, login_form: LoginForm) -> Token: ...

    @abstractmethod
    async def find_by_id(self, *, id: int) -> UserQuery: ...

    @abstractmethod
    async def export_user_template(self, file_name: str) -> StreamingResponse: ...

    @abstractmethod
    async def import_user(self, *, file: UploadFile): ...

    @abstractmethod
    async def export_user(self, *, params: Params, file_name: str) -> StreamingResponse: ...

    @abstractmethod
    async def retrieve_user(self, *, page: int, size: int, **kwargs) -> Optional[List[UserQuery]]: ...
