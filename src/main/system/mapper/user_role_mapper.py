"""UserRole operation mapper"""

from src.common.persistence.sqlmodel_impl import SqlModelMapper
from src.main.system.model.user_role_do import UserRoleDO


class UserRoleMapper(SqlModelMapper[UserRoleDO]):
    pass


userRoleMapper = UserRoleMapper(UserRoleDO)
