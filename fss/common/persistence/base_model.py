"""Common attributes for data object"""

from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger
from sqlmodel import SQLModel as _SQLModel, Field

from fss.common.util.snowflake import snowflake_id


class BaseModel(_SQLModel):
    id: int = Field(
        default_factory=snowflake_id,
        primary_key=True,
        index=True,
        nullable=False,
        sa_type=BigInteger,
    )


class ModelExt(_SQLModel):
    create_time: Optional[datetime] = Field(default_factory=datetime.now)
    update_time: Optional[datetime] = Field(
        default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now}
    )
