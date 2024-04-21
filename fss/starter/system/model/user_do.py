"""User data object"""

from typing import Optional

from sqlmodel import Field, Column, String, SQLModel

from fss.common.persistence.base_model import ModelExt, BaseModel


class BaseUser(SQLModel):
    username: str = Field(
        sa_column=Column(
            String(32), index=True, unique=True, nullable=True, comment="用户名"
        )
    )
    password: str = Field(
        default=None, sa_column=Column(String(64), nullable=True, comment="密码")
    )
    nickname: Optional[str] = Field(
        default=None, sa_column=Column(String(32), comment="昵称")
    )


class UserDO(ModelExt, BaseUser, BaseModel, table=True):
    __tablename__ = "sys_user"
    __table_args__ = {"comment": "用户信息表"}
