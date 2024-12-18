from sqlalchemy import BigInteger, Column, Index, UniqueConstraint
from sqlmodel import SQLModel, Field

from src.main.common.persistence.model_base import ModelExt, ModelBase


class UserRoleMeta(SQLModel):
    user_id: int = Field(sa_column=Column(BigInteger, nullable=True, comment="用户Id"))
    role_id: int = Field(sa_column=Column(BigInteger, nullable=True, comment="角色Id"))


class UserRoleDO(ModelExt, UserRoleMeta, ModelBase, table=True):
    __tablename__ = "sys_user_role"
    __table_args__ = (
        Index("idx_user_role_id", "user_id", "role_id"),
        UniqueConstraint("user_id", "role_id", name="uix_user_id_role_id"),
        {"comment": "用户角色关联表"},
    )
