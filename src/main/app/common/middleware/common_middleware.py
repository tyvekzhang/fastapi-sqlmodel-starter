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
"""Middleware module for FastAPI application."""

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.main.app.common.config.config_manager import load_config

server_config = load_config().server
security_config = load_config().security
database_config = load_config().database


def register_middleware(app: FastAPI) -> None:
    # Register CORS
    origins = [origin.strip() for origin in security_config.backend_cors_origins.split(",")]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register JWT
