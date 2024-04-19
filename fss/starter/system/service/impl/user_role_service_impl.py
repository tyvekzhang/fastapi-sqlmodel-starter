"""UserRole domain service impl"""

from fss.common.service.impl.service_impl import ServiceImpl
from fss.starter.system.mapper.user_role_mapper import UserRoleMapper, userRoleMapper
from fss.starter.system.model.user_role_do import UserRoleDO
from fss.starter.system.service.user_role_service import UserRoleService


class UserRoleServiceImpl(ServiceImpl[UserRoleMapper, UserRoleDO], UserRoleService):
    """
    Implementation of the UserRoleService interface.
    """

    pass


def get_user_role_service() -> UserRoleService:
    """
    Return an instance of the UserRoleService implementation.

    Returns:
        UserRoleService: An instance of the UserRoleServiceImpl class.
    """
    return UserRoleServiceImpl(mapper=userRoleMapper)
