"""UserRole operation mapper"""

from fss.common.persistence.sqlmodel_impl import SqlModelMapperBase
from fss.starter.system.model.user_role_do import UserRoleDO


class UserRoleMapper(SqlModelMapperBase[UserRoleDO]):
    pass


userRoleMapper = UserRoleMapper(UserRoleDO)
