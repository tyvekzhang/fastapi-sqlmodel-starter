"""UserRole domain service interface"""

from abc import ABC

from fss.common.service.service import Service
from fss.starter.system.model.user_role_do import UserRoleDO


class UserRoleService(Service[UserRoleDO], ABC):
    pass
