"""Role domain service interface"""

from abc import ABC

from fss.common.service.service import Service
from fss.starter.system.model.role_do import RoleDO


class RoleService(Service[RoleDO], ABC):
    pass
