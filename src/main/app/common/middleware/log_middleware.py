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
"""FastAPI Request Logging Middleware"""

import time
import uuid

from loguru import logger
from fastapi import Request


async def log_requests(request: Request, call_next):
    """Middleware to log all incoming requests and responses"""
    # Generate unique request ID
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    # Log request start information
    start_time = time.time()

    logger.info(
        "Request started",
        request_id=request_id,
        method=request.method,
        path=request.url.path,
        query_params=dict(request.query_params),
        client_ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )

    try:
        response = await call_next(request)
    except Exception as exc:
        # Log exception information
        logger.error("Request failed", request_id=request_id, exception=str(exc), exc_info=True)
        raise

    # Calculate processing time
    process_time = (time.time() - start_time) * 1000
    process_time = round(process_time, 2)

    # Log response information
    logger.info(
        "Request completed",
        request_id=request_id,
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        process_time=f"{process_time}ms",
    )

    # Add request ID to response headers
    response.headers["X-Request-ID"] = request_id
    return response
