"""Role domain service interface"""

from abc import ABC

from src.main.app.common.service.service_base import ServiceBase
from src.main.app.model.role_do import RoleDO


class RoleService(ServiceBase[RoleDO], ABC): ...
