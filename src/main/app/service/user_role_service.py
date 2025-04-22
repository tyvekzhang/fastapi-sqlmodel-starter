"""UserRole domain service interface"""

from abc import ABC
from typing import List

from src.main.app.common.service.service_base import ServiceBase
from src.main.app.model.user_role_do import UserRoleDO


class UserRoleService(ServiceBase[UserRoleDO], ABC):
    async def assign_roles(
        self,
        *,
        user_id: int,
        role_ids: List[int],
    ) -> bool: ...
