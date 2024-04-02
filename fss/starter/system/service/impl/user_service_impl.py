"""User domain service impl"""

from typing import Optional

from fss.common.service.impl.service_impl import ServiceImpl
from fss.starter.system.mapper.user_mapper import UserMapper
from fss.starter.system.model.user_do import UserDO
from fss.starter.system.schema.user_schema import UserQuery
from fss.starter.system.service.user_service import UserService


class UserServiceImpl(ServiceImpl[UserMapper, UserDO], UserService):
    def __init__(self, mapper: UserMapper):
        self.mapper = mapper

    async def find_by_id(self, id: int) -> Optional[UserQuery]:
        """
        Find a user by their ID and return a UserQuery instance.

        Args:
            id (int): The ID of the user to find.

        Returns:
            Optional[UserQuery]: A UserQuery instance if the user is found, otherwise None.
        """
        user_do = await self.mapper.select_by_id(id=id)
        if user_do:
            return UserQuery(**user_do.dict())
        else:
            return None


def get_user_service() -> UserService:
    return UserServiceImpl(UserMapper(UserDO))
