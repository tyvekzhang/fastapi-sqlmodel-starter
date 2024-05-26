"""Server init"""

import uvicorn
from fastapi_offline import FastAPIOffline
from starlette.middleware.cors import CORSMiddleware
from typing import Tuple

from fss.common.config import configs, init_log, server_startup_config

# Offline swagger docs
app = FastAPIOffline(
    title=configs.app_name,
    version=configs.version,
    openapi_url=f"{configs.api_version}/openapi.json",
    description=configs.app_desc,
    default_response_model_exclude_unset=True,
)

# Cors middleware
if configs.backend_cors_origins:
    origins = [origin.strip() for origin in configs.backend_cors_origins.split(",")]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def prepare() -> Tuple[str, int, int]:
    """
    Init log and extract server start option
    """
    init_log()
    return server_startup_config()


def run() -> None:
    """
    Server start
    """
    host, port, workers = prepare()
    uvicorn.run(app="fss.starter.server:app", host=host, port=port, workers=workers)
