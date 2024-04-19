"""Jwt middleware"""

import http

from fastapi import Request
from jose import JWTError
from loguru import logger
from starlette.responses import JSONResponse

from fss.common.config import configs
from fss.common.security.security import is_valid_token
from fss.starter.server import app


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
                status_code=http.HTTPStatus.FORBIDDEN,
                content={"detail": "The documentation isn't ready yet."},
            )
    white_list_routes = [
        router.strip() for router in configs.white_list_routes.split(",")
    ]
    request_url_path = configs.api_version + raw_url_path.split(configs.api_version)[1]
    if request_url_path in white_list_routes:
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if auth_header:
        try:
            token = auth_header.split(" ")[-1]
            await is_valid_token(token)
        except JWTError as e:
            logger.error(f"{e}")
            return JSONResponse(
                status_code=http.HTTPStatus.UNAUTHORIZED,
                content={"detail": "Invalid token or expired token"},
            )

    else:
        return JSONResponse(
            status_code=401,
            content={"detail": "Missing Authentication token"},
        )

    return await call_next(request)
