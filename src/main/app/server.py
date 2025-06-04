"""Server startup that include register router、session、cors、global exception handler、jwt, openapi..."""

import os
import subprocess
import time

from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles
from loguru import logger

from src.main.app.common.config.config_manager import load_config
from src.main.app.common.middleware import common_middleware
from src.main.app.common.middleware.db_session_middleware import SQLAlchemyMiddleware
from src.main.app.common.session.db_engine import get_async_engine
from src.main.app.common.util.work_path_util import resource_dir
from src.main.app.router.router import create_router

config = load_config()
server_config = config.server

# server setup config, eg: openapi, db, router, middleware, etc.
app = FastAPI(
    docs_url=None,
    redoc_url=None,
    title=server_config.name,
    version=server_config.version,
    description=server_config.app_desc,
)
common_middleware.register_middleware(app)
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