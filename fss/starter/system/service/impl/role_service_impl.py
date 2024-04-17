"""Role domain service impl"""

from fss.starter.system.mapper.role_mapper import RoleMapper, roleMapper

from fss.common.service.impl.service_impl import ServiceImpl
from fss.starter.system.model.role_do import RoleDO
from fss.starter.system.service.role_service import RoleService


class RoleServiceImpl(ServiceImpl[RoleMapper, RoleDO], RoleService):
    def __init__(self, mapper: RoleMapper):
        super(RoleServiceImpl, self).__init__(mapper=mapper)
        self.mapper = mapper


def get_role_service() -> RoleService:
    return RoleServiceImpl(mapper=roleMapper)
