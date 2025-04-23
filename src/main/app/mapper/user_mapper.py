"""User operation mapper"""

from typing import Union

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.main.app.common.mapper.impl.mapper_base_impl import SqlModelMapper
from src.main.app.entity.user_entity import UserEntity


class UserMapper(SqlModelMapper[UserEntity]):
    async def get_user_by_username(
        self, *, username: str, db_session: Union[AsyncSession, None] = None
    ) -> Union[UserEntity, None]:
        """
        Retrieve a user record by username.

        Args:
            username (str): The username to query.
            db_session (AsyncSession or None, optional): The database session instance. If None, use the default
            session.

        Returns:
            Union[UserEntity, None]: The UserEntity instance if found, otherwise None.
        """
        db_session = db_session or self.db.session
        response = await db_session.exec(select(UserEntity).where(UserEntity.username == username))
        return response.one_or_none()

    async def get_user_by_usernames(
        self, *, usernames: list[str], db_session: Union[AsyncSession, None] = None
    ) -> Union[list[UserEntity], None]:
        """
        Query user by usernames
        """
        db_session = db_session or self.db.session
        statement = select(UserEntity).where(UserEntity.username.in_(usernames))
        results = await db_session.exec(statement)
        return results.all()


userMapper = UserMapper(UserEntity)
