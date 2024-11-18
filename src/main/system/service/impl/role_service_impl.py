"""Role domain service impl"""

from src.main.system.mapper.role_mapper import RoleMapper

from src.common.service.impl.service_base_impl import ServiceBaseImpl
from src.main.system.model.role_do import RoleDO
from src.main.system.service.role_service import RoleService


class RoleServiceImpl(ServiceBaseImpl[RoleMapper, RoleDO], RoleService):
    """
    Implementation of the RoleService interface.
    """

    def __init__(self, mapper: RoleMapper):
        """
        Initialize the RoleServiceImpl instance.

        Args:
            mapper (RoleMapper): The RoleMapper instance to use for database operations.
        """
        super(RoleServiceImpl, self).__init__(mapper=mapper)
        self.mapper = mapper
