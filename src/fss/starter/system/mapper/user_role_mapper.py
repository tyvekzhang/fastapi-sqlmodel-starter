"""UserRole operation mapper"""

from fss.common.persistence.sqlmodel_impl import SqlModelMapper
from fss.starter.system.model.user_role_do import UserRoleDO


class UserRoleMapper(SqlModelMapper[UserRoleDO]):
    pass


userRoleMapper = UserRoleMapper(UserRoleDO)
