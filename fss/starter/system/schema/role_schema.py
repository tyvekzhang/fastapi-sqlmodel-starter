"""Role domain schema"""

from typing import Optional

from pydantic import BaseModel


class RoleCreateCmd(BaseModel):
    """
    RoleCreate schema
    """

    id: int = None
    name: str
    sort: int
    remark: Optional[str]


class RoleDeleteCmd(BaseModel):
    """
    RoleDelete schema
    """

    role_ids: list[int]
