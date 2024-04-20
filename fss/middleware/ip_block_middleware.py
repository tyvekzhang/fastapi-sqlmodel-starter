"""Ip block middleware"""

import http

from fastapi import Request
from starlette.responses import JSONResponse

from fss.starter.server import app


@app.middleware("http")
async def ip_block_middleware(request: Request, call_next):
    """
    Middleware to block requests from specific IP addresses.

    Args:
        request (Request): The incoming request.
        call_next (Callable): The next middleware or endpoint to call.

    Returns:
        Response: A 403 Forbidden response if the IP address is blocked.
    """
    client_host = request.client.host
    if client_host in []:
        return JSONResponse(
            status_code=http.HTTPStatus.FORBIDDEN,
            content={"detail": "Service unavailable, please contact administrator."},
        )
    return await call_next(request)
