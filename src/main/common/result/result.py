"""The results returned by the project"""

from typing import Generic, TypeVar, Optional, Dict

from pydantic import BaseModel

DataType = TypeVar("DataType")
T = TypeVar("T")

DEFAULT_SUCCESS_CODE: int = 0
DEFAULT_SUCCESS_MSG: str = "success"


class BaseResponse(BaseModel, Generic[T]):
    msg: str = ""
    code: Optional[int] = DEFAULT_SUCCESS_CODE
    data: Optional[T] = None


def success(
    data: DataType = None,
    msg: Optional[str] = "success",
    code: Optional[int] = DEFAULT_SUCCESS_CODE,
) -> Dict:
    if data is None:
        return {"code": code, "msg": msg}
    return {"code": code, "msg": msg, "data": data}


def fail(msg: str, code: int) -> Dict:
    return {"code": code, "msg": msg}
