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
"""User domain service impl"""

from __future__ import annotations
import io
from typing import Optional, List
from typing import Union
import pandas as pd
from fastapi import UploadFile, Request
from fastapi.exceptions import ResponseValidationError
from starlette.responses import StreamingResponse
from src.main.app.core.constant import FilterOperators
from src.main.app.core.utils import excel_util
from src.main.app.core.utils.validate_util import ValidateService
from src.main.app.mapper.sys_user_mapper import UserMapper
from src.main.app.model.sys_user_model import UserModel
from src.main.app.core.schema import PageResult
from src.main.app.schema.sys_user_schema import UserQuery, UserPage, UserDetail, UserCreate
from src.main.app.core.service.impl.base_service_impl import BaseServiceImpl
from src.main.app.service.sys_user_service import UserService


class UserServiceImpl(BaseServiceImpl[UserMapper, UserModel], UserService):
    """
    Implementation of the UserService interface.
    """

    def __init__(self, mapper: UserMapper):
        """
        Initialize the UserServiceImpl instance.

        Args:
            mapper (UserMapper): The UserMapper instance to use for database operations.
        """
        super().__init__(mapper=mapper)
        self.mapper = mapper

    async def fetch_user_by_page(self, user_query: UserQuery, request: Request) -> PageResult:
        eq = {}
        ne = {}
        gt = {}
        ge = {}
        lt = {}
        le = {}
        between = {}
        like = {}
        if user_query.id is not None and user_query.id != "" :
            eq["id"] = user_query.id
        if user_query.username is not None and user_query.username != "" :
            like["username"] = user_query.username
        if user_query.password is not None and user_query.password != "" :
            eq["password"] = user_query.password
        if user_query.nickname is not None and user_query.nickname != "" :
            like["nickname"] = user_query.nickname
        if user_query.avatar_url is not None and user_query.avatar_url != "" :
            eq["avatar_url"] = user_query.avatar_url
        if user_query.status is not None and user_query.status != "" :
            eq["status"] = user_query.status
        if user_query.remark is not None and user_query.remark != "" :
            eq["remark"] = user_query.remark
        if user_query.create_time is not None and user_query.create_time != "" :
            eq["create_time"] = user_query.create_time
        filters = {
            FilterOperators.EQ: eq,
            FilterOperators.NE: ne,
            FilterOperators.GT: gt,
            FilterOperators.GE: ge,
            FilterOperators.LT: lt,
            FilterOperators.LE: le,
            FilterOperators.BETWEEN: between,
            FilterOperators.LIKE: like
        }
        records, total = await self.mapper.select_by_ordered_page(
            current=user_query.current,
            pageSize=user_query.pageSize,
            **filters
        )
        if total == 0:
            return PageResult(records=[], total=total)
        if "sort" in UserModel.model_fields and total > 1:
            records.sort(key=lambda x: x['sort'])
        records = [UserPage(**record.model_dump()) for record in records]
        return PageResult(records=records, total=total)

    async def fetch_user_detail(self, *, id: int, request: Request) -> Optional[UserDetail]:
        user_do: UserModel =await self.mapper.select_by_id(id=id)
        if user_do is None:
            return None
        return UserDetail(**user_do.model_dump())

    async def export_user_page(self, *, ids: List[int], request: Request) -> Optional[StreamingResponse]:
        if ids is None or len(ids) == 0:
            return None
        user_list: List[UserModel] = await self.retrieve_by_ids(ids = ids)
        if user_list is None or len(user_list) == 0:
            return None
        user_page_list = [UserPage(**user.model_dump()) for user in user_list]
        return await excel_util.export_excel(schema=UserPage, file_name="user_data_export", data_list=user_page_list)

    async def create_user(self, user_create: UserCreate, request: Request) -> UserModel:
        user: UserModel = UserModel(**user_create.model_dump())
        # user.user_id = request.state.user_id
        return await self.save(data=user)

    async def batch_create_user(self, *, user_create_list: List[UserCreate], request: Request) -> List[int]:
        user_list: List[UserModel] = [UserModel(**user_create.model_dump()) for user_create in user_create_list]
        await self.batch_save(datas=user_list)
        return [user.id for user in user_list]

    @staticmethod
    async def import_user(*, file: UploadFile, request: Request) -> Union[List[UserCreate], None]:
        contents = await file.read()
        import_df = pd.read_excel(io.BytesIO(contents))
        import_df = import_df.fillna("")
        user_records = import_df.to_dict(orient="records")
        if user_records is None or len(user_records) == 0:
            return None
        for record in user_records:
            for key, value in record.items():
                if value == "":
                    record[key] = None
        user_create_list = []
        for user_record in user_records:
            try:
                user_create = UserCreate(**user_record)
                user_create_list.append(user_create)
            except Exception as e:
                valid_data = {k: v for k, v in user_record.items() if k in UserCreate.model_fields}
                user_create = UserCreate.model_construct(**valid_data)
                user_create.err_msg = ValidateService.get_validate_err_msg(e)
                user_create_list.append(user_create)
                return user_create_list

        return user_create_list