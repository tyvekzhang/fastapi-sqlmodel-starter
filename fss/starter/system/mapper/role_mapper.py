"""Role operation mapper"""

from fss.common.persistence.sqlmodel_impl import SqlModelMapper
from fss.starter.system.model.role_do import RoleDO


class RoleMapper(SqlModelMapper[RoleDO]):
    pass


roleMapper = RoleMapper(RoleDO)
