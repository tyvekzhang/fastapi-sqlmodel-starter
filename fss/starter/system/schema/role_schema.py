"""Role domain schema"""

from typing import Optional

from pydantic import BaseModel


class RoleCreateCmd(BaseModel):
    """
    RoleCreate schema
    """

    name: str
    sort: int
    remark: Optional[str]
