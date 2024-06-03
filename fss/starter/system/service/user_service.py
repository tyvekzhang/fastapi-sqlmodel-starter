"""User domain service interface"""

from abc import ABC, abstractmethod
from typing import Optional, List

from fastapi import UploadFile
from fastapi_pagination import Params
from starlette.responses import StreamingResponse

from fss.common.schema.schema import Token
from fss.common.service.service import Service
from fss.starter.system.model.user_do import UserDO
from fss.starter.system.schema.user_schema import UserQuery, LoginCmd


class UserService(Service[UserDO], ABC):
    @abstractmethod
    async def find_by_id(self, id: int) -> UserQuery: ...

    @abstractmethod
    async def login(self, loginCmd: LoginCmd) -> Token: ...

    @abstractmethod
    async def export_user_template(self) -> StreamingResponse: ...

    @abstractmethod
    async def import_user(self, file: UploadFile): ...

    @abstractmethod
    async def export_user(self, params: Params) -> StreamingResponse: ...

    @abstractmethod
    async def register(self, record) -> UserDO: ...

    @abstractmethod
    async def retrieve_user(
        self, page: int, size: int
    ) -> Optional[List[UserQuery]]: ...
