"""Server init"""

import uvicorn
from fastapi_offline import FastAPIOffline
from starlette.middleware.cors import CORSMiddleware

from fss.common.config import configs, port, workers

app = FastAPIOffline(
    title=configs.app_name,
    version=configs.version,
    openapi_url=f"{configs.api_version}/openapi.json",
    description=configs.app_desc,
    default_response_model_exclude_unset=True,
)

if configs.backend_cors_origins:
    """
    Cors processing
    """
    origins = [origin.strip() for origin in configs.backend_cors_origins.split(",")]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def run() -> None:
    uvicorn.run(
        app="fss.starter.server:app", host=configs.host, port=port, workers=workers
    )
