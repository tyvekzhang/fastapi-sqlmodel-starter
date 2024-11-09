"""UserRole domain service impl"""

from typing import List

from fss.common.service.impl.service_base_impl import ServiceBaseImpl
from fss.starter.system.mapper.user_role_mapper import UserRoleMapper
from fss.starter.system.model.user_role_do import UserRoleDO
from fss.starter.system.service.user_role_service import UserRoleService


class UserRoleServiceImpl(ServiceBaseImpl[UserRoleMapper, UserRoleDO], UserRoleService):
    """
    Implementation of the UserRoleService interface.
    """

    async def assign_roles(
        self,
        *,
        user_id: int,
        role_ids: List[int],
    ) -> bool:
        """
        Assign roles to a user

        Args:
            user_id: ID of the user to assign roles to.

            role_ids: List of role IDs to assign to the user.
        """
        if len(role_ids) == 0:
            return
        user_roles = [
            UserRoleDO(user_id=user_id, role_id=role_id) for role_id in role_ids
        ]
        await self.mapper.batch_insert(records=user_roles)
