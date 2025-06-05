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
"""Server startup that include register router、session、cors、global exception handler、jwt, openapi..."""

import os
import subprocess
import time

from fastapi import FastAPI
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from src.main.app.common.config.config_manager import load_config
from src.main.app.common.exception import common_exception
from src.main.app.common.middleware.jwt_middleware import jwt_middleware
from src.main.app.common.openapi import offline
from src.main.app.common.session.db_engine import get_async_engine
from src.main.app.common.session.db_session_middleware import SQLAlchemyMiddleware
from src.main.app.common.constants.common_constant import RESOURCE_DIR
from src.main.app.router.router import create_router

# Load config
config = load_config()
server_config = config.server
security_config = config.security

# Setup timezone
if os.name == "nt":
    subprocess.run(["tzutil", "/s", server_config.win_tz], check=True)

else:
    os.environ["TZ"] = server_config.linux_tz
    time.tzset()

# Setup log
logger.add(
    server_config.log_file_path,
    rotation="10 MB",
    retention="30 days",
    compression="zip",
    level="DEBUG" if server_config.debug else "INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)

# Setup fastapi instance
app = FastAPI(
    docs_url=None,
    redoc_url=None,
    title=server_config.name,
    version=server_config.version,
    description=server_config.app_desc,
)

# Register middleware
app.add_middleware(SQLAlchemyMiddleware, custom_engine=get_async_engine())
origins = [origin.strip() for origin in security_config.backend_cors_origins.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(jwt_middleware)

# Register exception handler
common_exception.register_exception_handlers(app)

# Setup router
router = create_router()
app.include_router(router, prefix=server_config.api_version)

# Register offline openapi
offline.register_offline_openapi(app=app, resource_dir=RESOURCE_DIR)
