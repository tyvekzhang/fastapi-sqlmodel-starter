"""Role operation mapper"""

from src.main.app.common.mapper.impl.mapper_base_impl import SqlModelMapper
from src.main.app.model.role_do import RoleDO


class RoleMapper(SqlModelMapper[RoleDO]):
    pass


roleMapper = RoleMapper(RoleDO)
