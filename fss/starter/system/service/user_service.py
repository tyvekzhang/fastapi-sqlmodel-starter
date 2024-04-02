"""User domain service interface"""

from abc import ABC, abstractmethod

from fss.common.service.service import Service
from fss.starter.system.model.user_do import UserDO
from fss.starter.system.schema.user_schema import UserQuery


class UserService(Service[UserDO], ABC):
    @abstractmethod
    async def find_by_id(self, id: int) -> UserQuery:
        raise NotImplementedError
