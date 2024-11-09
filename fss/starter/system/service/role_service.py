"""Role domain service interface"""

from abc import ABC

from fss.common.service.service_base import ServiceBase
from fss.starter.system.model.role_do import RoleDO


class RoleService(ServiceBase[RoleDO], ABC): ...
