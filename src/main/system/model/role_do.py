"""Role data object"""

from typing import Optional

from sqlmodel import Field, Column, Integer, String, SQLModel

from src.main.common.persistence.model_base import ModelExt, ModelBase


class BaseRole(SQLModel):
    name: str = Field(sa_column=Column(String(32), index=True, nullable=True, comment="角色名"))
    sort: int = Field(sa_column=Column(Integer, nullable=True, comment="排序"))

    remark: Optional[str] = Field(default=None, sa_column=Column(String, comment="备注信息"))


class RoleDO(ModelExt, BaseRole, ModelBase, table=True):
    __tablename__ = "sys_role"
    __table_args__ = {"comment": "角色信息表"}
