"""UserRole operation mapper"""

from src.main.app.common.mapper.impl.mapper_base_impl import SqlModelMapper
from src.main.app.model.user_role_do import UserRoleDO


class UserRoleMapper(SqlModelMapper[UserRoleDO]):
    pass


userRoleMapper = UserRoleMapper(UserRoleDO)
