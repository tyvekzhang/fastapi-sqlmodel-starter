"""User domain service interface"""

from abc import ABC, abstractmethod
from typing import Optional, List

from fastapi import UploadFile
from fastapi_pagination import Params
from starlette.responses import StreamingResponse

from src.common.schema.schema import Token
from src.common.service.service_base import ServiceBase
from src.main.system.model.user_do import UserDO
from src.main.system.schema.user_schema import UserQuery, LoginCmd


class UserService(ServiceBase[UserDO], ABC):
    @abstractmethod
    async def register(self, *, user_create_cmd) -> UserDO: ...

    @abstractmethod
    async def login(self, *, login_cmd: LoginCmd) -> Token: ...

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
