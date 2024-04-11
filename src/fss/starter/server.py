"""Server init"""

import uvicorn
from fastapi import Request
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from fastapi.utils import is_body_allowed_for_status_code
from fastapi_offline import FastAPIOffline
from jose import JWTError
from loguru import logger
from sqlalchemy import NullPool
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, Response

from fss.common import config
from fss.common.config import configs
from fss.common.exception.exception import ServiceException
from fss.common.util.security import is_valid_token
from fss.middleware.db_session_middleware import SQLAlchemyMiddleware
from fss.starter.system.router.system import system_router

# FastAPIOffline setting
app = FastAPIOffline(
    title=configs.app_name,
    openapi_url=f"{configs.api_version}/openapi.json",
    description=configs.app_desc,
    default_response_model_exclude_unset=True,
)

# Add project routing
app.include_router(system_router, prefix=configs.api_version)

# Add SQLAlchemyMiddleware
app.add_middleware(
    SQLAlchemyMiddleware,
    db_url=str(configs.sqlalchemy_database_url),
    engine_args={"echo": True, "poolclass": NullPool},
)


# Global exception handling
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
    logger.error(
        f"Exception occurred: {exc} \n"
        f"Request path: {request.url.path} \n"
        f"Request method: {request.method} \n"
        f"Request headers: {request.headers} \n"
        f"Request body: {await request.body()}"
    )
    headers = getattr(exc, "headers", None)
    if not is_body_allowed_for_status_code(exc.status_code):
        return Response(status_code=exc.status_code, headers=headers)
    return JSONResponse(
        {"code": exc.code, "detail": exc.detail},
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
    logger.error(
        f"Exception occurred: {exc} \n"
        f"Request path: {request.url.path} \n"
        f"Request method: {request.method} \n"
        f"Request headers: {request.headers} \n"
        f"Request body: {await request.body()}"
    )
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Asynchronous handler for RequestValidationError
    :param request: The request instance containing all request details
    :param exc: StarletteHTTPException instance
    :return: A Starlette Response object.
    """
    logger.error(
        f"Exception occurred: {exc} \n"
        f"Request path: {request.url.path} \n"
        f"Request method: {request.method} \n"
        f"Request headers: {request.headers} \n"
        f"Request body: {await request.body()}"
    )
    return await request_validation_exception_handler(request, exc)


WHITE_LIST_ROUTES = set()
for router in configs.white_list_routes.split(","):
    WHITE_LIST_ROUTES.add(router.strip())


# Jwt middleware
@app.middleware("http")
async def jwt_middleware(request: Request, call_next):
    raw_url_path = request.url.path
    if not raw_url_path.__contains__(configs.api_version) or raw_url_path.__contains__(
        ".json"
    ):
        if configs.enable_swagger:
            return await call_next(request)
        else:
            return JSONResponse(
                status_code=403,
                content={"detail": "The documentation isn't ready yet."},
            )
    request_url_path = configs.api_version + raw_url_path.split(configs.api_version)[1]
    if request_url_path in WHITE_LIST_ROUTES:
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if auth_header:
        try:
            token = auth_header.split(" ")[-1]
            await is_valid_token(token)
        except JWTError as e:
            logger.error(f"{e}")
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid token or expired token"},
            )

    else:
        return JSONResponse(
            status_code=401,
            content={"detail": "Missing Authentication token"},
        )

    return await call_next(request)


# Cors processing
if configs.backend_cors_origins:
    origins = []
    for origin in configs.backend_cors_origins.split(","):
        origins.append(origin.strip())
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# Prepare run
def prepare_run():
    config.init_log()
    config.init_tz()
    return config.complete()


# Project run
def run() -> None:
    port, workers = prepare_run()
    uvicorn.run(
        app="fss.starter.server:app", host="0.0.0.0", port=port, workers=workers
    )
