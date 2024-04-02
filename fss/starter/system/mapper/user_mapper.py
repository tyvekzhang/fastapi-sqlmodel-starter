"""User operation mapper"""

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from fss.common.persistence.sqlmodel_impl import SqlModelMapper
from fss.starter.system.model.user_do import UserDO


class UserMapper(SqlModelMapper[UserDO]):
    async def get_user_by_username(
        self, *, username: str, db_session: AsyncSession | None = None
    ) -> UserDO | None:
        """
        Retrieve a user record by username.

        Args:
            username (str): The username to query.
            db_session (AsyncSession | None, optional): The database session instance. If None, use the default session.

        Returns:
            UserDO | None: The UserDO instance if found, otherwise None.
        """
        db_session = db_session or self.db.session
        user = await db_session.execute(
            select(UserDO).where(UserDO.username == username)
        )
        return user.scalar_one_or_none()


userMapper = UserMapper(UserDO)
