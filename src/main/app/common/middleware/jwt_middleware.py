# Copyright (c) 2025 Fast web and/or its affiliates. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Jwt middleware"""

import http

from fastapi import Request
from jose import JWTError
from loguru import logger
from starlette.responses import JSONResponse

from src.main.app.common.config.config_manager import load_config
from src.main.app.common.security import common_security

config = load_config()


async def jwt_middleware(request: Request, call_next):
    raw_url_path = request.url.path
    if not raw_url_path.__contains__(config.server.api_version) or raw_url_path.__contains__(".json"):
        if config.security.enable_swagger:
            return await call_next(request)
        else:
            return JSONResponse(
                status_code=http.HTTPStatus.FORBIDDEN,
                content={"detail": "The documentation isn't ready yet."},
            )
    white_list_routes = [router.strip() for router in config.security.white_list_routes.split(",")]
    request_url_path = config.server.api_version + raw_url_path.split(config.server.api_version)[1]
    if request_url_path in white_list_routes:
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if auth_header:
        try:
            token = auth_header.split(" ")[-1]
            await common_security.validate_token(token)
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
