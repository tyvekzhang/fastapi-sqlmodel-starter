"""Role operation mapper"""

from fss.common.persistence.sqlmodel_impl import SqlModelMapperBase
from fss.starter.system.model.role_do import RoleDO


class RoleMapper(SqlModelMapperBase[RoleDO]):
    pass


roleMapper = RoleMapper(RoleDO)
