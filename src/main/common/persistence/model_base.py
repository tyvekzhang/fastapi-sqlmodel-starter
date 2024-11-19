"""Common attributes for data object"""

from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger
from sqlmodel import SQLModel as _SQLModel, Field

from src.main.common.util.snowflake import snowflake_id


class ModelBase(_SQLModel):
    """
    Identifier for a data object
    """

    id: int = Field(
        default_factory=snowflake_id,
        primary_key=True,
        sa_type=BigInteger,
        sa_column_kwargs={"comment": "主键"},
    )


class ModelExt(_SQLModel):
    """
    Create time and update time for a data object, can be automatically generated
    """

    create_time: Optional[int] = Field(
        sa_type=BigInteger,
        default_factory=lambda: int(datetime.now().timestamp()),
        sa_column_kwargs={"comment": "创建时间"},
    )
    update_time: Optional[int] = Field(
        sa_type=BigInteger,
        default_factory=lambda: int(datetime.now().timestamp()),
        sa_column_kwargs={
            "onupdate": lambda: int(datetime.now().timestamp()),
            "comment": "更新时间",
        },
    )
