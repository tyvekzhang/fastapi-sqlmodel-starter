"""Server startup that include register router、session、cors、global exception handler、jwt, openapi..."""

import http
import os
import subprocess
import time

from fastapi import FastAPI
from fastapi import Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles
from fastapi.utils import is_body_allowed_for_status_code
from jwt import PyJWTError
from loguru import logger
from pydantic_core._pydantic_core import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, Response

from src.main.app.common.config.config_manager import load_config
from src.main.app.common.enums.enum import ConstantCode
from src.main.app.common.enums.enum import ResponseCode
from src.main.app.common.exception.exception import ServiceException
from src.main.app.common.session.db_engine import get_async_engine
from src.main.app.common.session.db_session_middleware import SQLAlchemyMiddleware
from src.main.app.common.util.security_util import get_user_id
from src.main.app.common.util.work_path_util import resource_dir
from src.main.app.router.router import create_router

config = load_config()
server_config = config.server

# server setup config, eg: openapi, cors, router, middleware, etc.
app = FastAPI(
    docs_url=None,
    redoc_url=None,
    title=server_config.name,
    version=server_config.version,
    description=server_config.app_desc,
)
app.add_middleware(SQLAlchemyMiddleware, custom_engine=get_async_engine())
app.mount("/static", StaticFiles(directory=os.path.join(resource_dir, "static")), name="static")

logger.add(server_config.log_file_path)

# Set timezone
if os.name == "nt":
    subprocess.run(["tzutil", "/s", server_config.win_tz], check=True)

else:
    os.environ["TZ"] = server_config.linux_tz
    time.tzset()

router = create_router()
app.include_router(router, prefix=server_config.api_version)

origins = [origin.strip() for origin in config.security.backend_cors_origins.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        swagger_favicon_url="/static/favicon.png",
        openapi_url=app.openapi_url,
        title=config.server.name,
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        redoc_favicon_url="/static/favicon.png",
        openapi_url=app.openapi_url,
        title=config.server.name,
        redoc_js_url="/static/redoc.standalone.js",
    )


# global exception handler
@app.middleware("http")
async def jwt_middleware(request: Request, call_next):
    media_type_json = ".json"
    security = config.security
    if not security.enable:
        return await call_next(request)
    api_version = server_config.api_version
    raw_url_path = request.url.path
    if not raw_url_path.__contains__(api_version) or raw_url_path.__contains__(media_type_json):
        if security.enable_swagger:
            return await call_next(request)
        else:
            return JSONResponse(
                status_code=http.HTTPStatus.FORBIDDEN,
                content={"detail": "Document not enabled"},
            )
    white_list_routes = (url.strip() for url in security.white_list_routes.split(","))
    request_url_path = api_version + raw_url_path.split(api_version)[1]
    if request_url_path in white_list_routes:
        return await call_next(request)

    auth_header = request.headers.get(ConstantCode.AUTH_KEY)
    if auth_header:
        try:
            token = auth_header.split(" ")[-1]
            user_id = get_user_id(token)
            request.state.user_id = user_id
        except Exception as e:
            logger.error(f"{e}")
            return JSONResponse(
                status_code=http.HTTPStatus.UNAUTHORIZED,
                content={"detail": "Invalid token or expired token"},
            )

    else:
        return JSONResponse(
            status_code=http.HTTPStatus.UNAUTHORIZED,
            content={"detail": "Missing Authentication header"},
        )

    return await call_next(request)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Asynchronous exception handler for all unhandled exceptions.

    Args:
        request (Request): The request instance containing all request details.
        exc (Exception): The exception instance.

    Returns:
        Response: A Response object which could be a basic Response or a JSONResponse,
                  depending on whether a response body is allowed for the given status code.
    """
    status_code = http.HTTPStatus.INTERNAL_SERVER_ERROR
    headers = getattr(exc, "headers", None)
    if not is_body_allowed_for_status_code(status_code):
        return Response(status_code=status_code, headers=headers)
    return JSONResponse(
        {"code": ResponseCode.SERVICE_INTERNAL_ERROR.code, "msg": str(exc)},
        status_code=status_code,
    )


@app.exception_handler(ValidationError)
async def validation_exception_handler(exc: ValidationError):
    """
    Asynchronous exception handler for validation exceptions.

    Args:
        request (Request): The request instance containing all request details.
        exc (ValidationError): The exception instance.

    Returns:
        Response: A Response object which could be a basic Response or a JSONResponse,
                  depending on whether a response body is allowed for the given status code.
    """
    status_code = http.HTTPStatus.INTERNAL_SERVER_ERROR
    headers = getattr(exc, "headers", None)
    if not is_body_allowed_for_status_code(status_code):
        return Response(status_code=status_code, headers=headers)
    return JSONResponse(
        {
            "code": ResponseCode.SERVICE_INTERNAL_ERROR.code,
            "msg": str(exc).split("For further")[0],
        },
        status_code=status_code,
    )


@app.exception_handler(ServiceException)
async def service_exception_handler(request: Request, exc: ServiceException):
    """
    Asynchronous handler for ServiceException.

    Args:
        request (Request): The request instance containing all request details.
        exc (ServiceException): The ServiceException instance.

    Returns:
        Response: A Response object which could be a basic Response or a JSONResponse,
                  depending on whether a response body is allowed for the given status code.
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
    Asynchronous handler for StarletteHTTPException.

    Args:
        request (Request): The request instance containing all request details.
        exc (StarletteHTTPException): The StarletteHTTPException instance.

    Returns:
        Response: A Response object which could be a basic Response or a JSONResponse,
                  depending on whether a response body is allowed for the given status code.
    """
    return await http_exception_handler(request, exc)


@app.exception_handler(PyJWTError)
async def jwt_exception_handler() -> JSONResponse:
    """
    Asynchronous handler for JWT-related exceptions.

    Returns:
        JSONResponse: A JSON response with an error code and message.
    """
    return JSONResponse(
        status_code=http.HTTPStatus.UNAUTHORIZED,
        content={
            "code": http.HTTPStatus.UNAUTHORIZED,
            "msg": "Your token has expired. Please log in again.",
        },
    )
