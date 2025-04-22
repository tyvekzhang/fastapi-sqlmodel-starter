"""Role domain service impl"""

from src.main.app.common.service.impl.service_base_impl import ServiceBaseImpl
from src.main.app.mapper.role_mapper import RoleMapper

from src.main.app.model.role_do import RoleDO
from src.main.app.service.role_service import RoleService


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
