"""The results returned by the project"""

from typing import Sequence
from math import ceil
from typing import Generic, TypeVar, Any, Optional

from fastapi_pagination import Params, Page
from fastapi_pagination.bases import AbstractPage, AbstractParams
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


class IPage(AbstractPage[T], Generic[T]):
    msg: Optional[str] = ""
    code: Optional[int] = DEFAULT_SUCCESS_CODE
    data: PageBase[T]

    __params_type__ = Params

    @classmethod
    def create(
        cls,
        items: Sequence[T],
        total: int,
        params: AbstractParams,
    ) -> Optional[PageBase[T]]:
        if params.size is not None and total is not None and params.size != 0:
            pages = ceil(total / params.size)
        else:
            pages = 0

        return cls(
            data=PageBase[T](
                items=items,
                page=params.page,
                size=params.size,
                total=total,
                pages=pages,
                next_page=params.page + 1 if params.page < pages else None,
                previous_page=params.page - 1 if params.page > 1 else None,
            )
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
