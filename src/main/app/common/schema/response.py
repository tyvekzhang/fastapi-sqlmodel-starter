from typing import Generic, TypeVar, Optional, Any

from pydantic import BaseModel

# Define generic model variables
DataType = TypeVar("DataType")
T = TypeVar("T")

# Define default response codes and messages
DEFAULT_SUCCESS_CODE: int = 0
DEFAULT_FAIL_CODE: int = -1
DEFAULT_SUCCESS_MSG: str = "success"


class HttpResponse(BaseModel, Generic[T]):
    """
    Standardized API response model with success/fail static constructors.

    Attributes:
        msg: Human-readable response message
        code: HTTP status code or custom business code
        data: Optional response payload of type T
    """
    msg: str = DEFAULT_SUCCESS_MSG
    code: int = DEFAULT_SUCCESS_CODE
    data: Optional[T] = None

    @staticmethod
    def success(data: Optional[T] = None,
                msg: str = DEFAULT_SUCCESS_MSG,
                code: int = DEFAULT_SUCCESS_CODE) -> "HttpResponse[T]":
        """
        Quick constructor for success responses.

        Args:
            data: Response payload (optional)
            msg: Success message (default: 'success')
            code: Status code (default: 200)

        Returns:
            HttpResponse[T]: Success response instance
        """
        return HttpResponse[T](msg=msg, code=code, data=data)

    @staticmethod
    def fail(msg: str = str,
             code: int = DEFAULT_FAIL_CODE,
             data: Optional[Any] = None) -> "HttpResponse[Any]":
        """
        Quick constructor for error responses.

        Args:
            msg: Error message (default: 'error')
            code: Error code (default: -1)
            data: Additional error details (optional)

        Returns:
            HttpResponse[Any]: Error response instance
        """
        return HttpResponse[Any](msg=msg, code=code, data=data)
