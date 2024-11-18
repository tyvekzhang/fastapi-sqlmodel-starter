"""Role operation mapper"""

from src.common.persistence.sqlmodel_impl import SqlModelMapper
from src.main.system.model.role_do import RoleDO


class RoleMapper(SqlModelMapper[RoleDO]):
    pass


roleMapper = RoleMapper(RoleDO)
