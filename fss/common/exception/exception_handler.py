"""Global exception handler"""

from fastapi import Request
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from fastapi.utils import is_body_allowed_for_status_code
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse, Response

from fss.common.exception.exception import ServiceException
from fss.starter.server import app


@app.exception_handler(ServiceException)
async def service_exception_handler(request: Request, exc: ServiceException):
    """
    Asynchronous serviceException handler
    :param request: The request instance containing all request details
    :param exc: ServiceException instance
    :return: A Starlette Response object that could be a basic Response or a
                JSONResponse, depending on whether a response body is allowed for
                the given status code.
    """
    headers = getattr(exc, "headers", None)
    if not is_body_allowed_for_status_code(exc.status_code):
        return Response(status_code=exc.status_code, headers=headers)
    return JSONResponse(
        {"code": exc.code, "msg": exc.msg},
        status_code=exc.status_code,
        headers=headers,
    )


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Asynchronous handler for StarletteHTTPException
    :param request: The request instance containing all request details
    :param exc: StarletteHTTPException instance
    :return: A Starlette Response object that could be a basic Response or a
                JSONResponse, depending on whether a response body is allowed for
                the given status code.
    """
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Asynchronous handler for RequestValidationError
    :param request: The request instance containing all request details
    :param exc: RequestValidationError instance
    :return: A Starlette Response object.
    """
    return await request_validation_exception_handler(request, exc)
