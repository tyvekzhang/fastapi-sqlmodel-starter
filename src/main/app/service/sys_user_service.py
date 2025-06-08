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
"""User Service"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, List
from fastapi import UploadFile, Request
from starlette.responses import StreamingResponse
from src.main.app.model.sys_user_model import UserModel
from src.main.app.core.schema import PageResult
from src.main.app.schema.sys_user_schema import UserQuery, UserDetail, UserCreate
from src.main.app.core.service.base_service import BaseService


class UserService(BaseService[UserModel], ABC):

    @abstractmethod
    async def fetch_user_by_page(self, *, user_query: UserQuery, request: Request) -> PageResult:...

    @abstractmethod
    async def fetch_user_detail(self, *, id: int, request: Request) -> Optional[UserDetail]:...

    @abstractmethod
    async def export_user_page(self, *, ids: List[int], request: Request) -> Optional[StreamingResponse]:...

    @abstractmethod
    async def create_user(self, *, user_create: UserCreate, request: Request) -> UserModel:...

    @abstractmethod
    async def batch_create_user(self, *, user_create_list: List[UserCreate], request: Request) -> List[int]:...

    @abstractmethod
    async def import_user(self, *, file: UploadFile, request: Request) -> List[UserCreate]:...