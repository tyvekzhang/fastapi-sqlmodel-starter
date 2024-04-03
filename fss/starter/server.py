"""Server init"""

import uvicorn
from fastapi_offline import FastAPIOffline
from loguru import logger
from sqlalchemy import NullPool
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from fss.common.config import configs
from fss.common import config
from fss.middleware.db_session_middleware import SQLAlchemyMiddleware
from fss.starter.system.router.system import system_router

# FastAPIOffline setting
app = FastAPIOffline(
    title=configs.app_name,
    openapi_url=f"{configs.api_version_v1}/openapi.json",
    description=configs.app_desc,
    default_response_model_exclude_unset=True,
)

# Add project routing
app.include_router(system_router, prefix=configs.api_version_v1)

# Add SQLAlchemyMiddleware
app.add_middleware(
    SQLAlchemyMiddleware,
    db_url=str(configs.sqlalchemy_database_url),
    engine_args={"echo": True, "poolclass": NullPool},
)


# Global exception handling
@app.exception_handler(Exception)
async def exception_handler(request, exc):
    logger.error(f"Exception occurred: {exc}")
    logger.error(f"Request path: {request.url.path}")
    logger.error(f"Request method: {request.method}")
    logger.error(f"Request headers: {request.headers}")
    logger.error(f"Request body: {await request.body()}")
    return JSONResponse(
        status_code=-1,
        content={
            "msg": "Please retry later. If the error still exists, please contact the administrator."
        },
    )


# Cross domain processing
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
