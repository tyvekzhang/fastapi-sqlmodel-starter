"""The results returned by the project"""

from typing import Generic, TypeVar, Any, Optional

from fastapi_pagination import Page
from pydantic import Field, BaseModel

DataType = TypeVar("DataType")
T = TypeVar("T")

DEFAULT_SUCCESS_CODE: int = 0
DEFAULT_SUCCESS_MSG: str = "success"


class BaseResponse(BaseModel, Generic[T]):
    msg: str = ""
    code: Optional[int] = DEFAULT_SUCCESS_CODE
    data: Optional[T] = None


class PageBase(Page[T], Generic[T]):
    previous_page: Optional[int] = Field(
        default=None, description="Page number of the previous page"
    )
    next_page: Optional[int] = Field(
        default=None, description="Page number of the next page"
    )


def success(
    data: DataType = None,
    msg: Optional[str] = "success",
    code: Optional[int] = DEFAULT_SUCCESS_CODE,
) -> Any:
    if data is None:
        return {"code": code, "msg": msg}
    return {"code": code, "msg": msg, "data": data}


def fail(msg: str, code: int) -> Any:
    return {"code": code, "msg": msg}
