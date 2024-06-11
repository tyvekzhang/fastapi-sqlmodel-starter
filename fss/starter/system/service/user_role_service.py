"""UserRole domain service interface"""

from abc import ABC
from typing import List

from fss.common.service.service import Service
from fss.starter.system.model.user_role_do import UserRoleDO


class UserRoleService(Service[UserRoleDO], ABC):
    async def assign_roles(
        self,
        *,
        user_id: int,
        role_ids: List[int],
    ) -> bool: ...
