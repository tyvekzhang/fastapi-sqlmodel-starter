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
"""User REST Controller"""

from typing import Annotated, List

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Query, UploadFile, Form, Request, Depends
from starlette.responses import StreamingResponse

from src.main.app.core.schema import HttpResponse, Token, CurrentUser
from src.main.app.core.schema import PageResult
from src.main.app.core.security import get_current_user
from src.main.app.core.utils import excel_util
from src.main.app.mapper.sys_user_mapper import userMapper
from src.main.app.model.sys_user_model import UserModel
from src.main.app.schema.sys_user_schema import UserQuery, UserModify, UserCreate, \
    UserBatchModify, UserDetail, LoginForm, UserPage
from src.main.app.service.impl.sys_user_service_impl import UserServiceImpl
from src.main.app.service.sys_user_service import UserService

user_router = APIRouter()
user_service: UserService = UserServiceImpl(mapper=userMapper)


@user_router.post("/login")
async def login(
        login_form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    """
    Authenticates user and provides an access token.

    Args:
        login_form_data: Login credentials.

    Returns:
        Token object with access token.
    """
    login_form = LoginForm(username=login_form_data.username, password=login_form_data.password)

    return await user_service.login(login_form=login_form)


@user_router.get("/me")
async def me(
        current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse[UserPage]:
    """
    Retrieves the profile of the current user.

    Args:
        current_user: Currently authenticated user.

    Returns:
        BaseResponse with current user's profile information.
    """
    user_page: UserPage = await user_service.find_by_id(id=current_user.user_id)
    return HttpResponse.success(user_page)


@user_router.get("/page")
async def get_user_by_page(
        user_query: Annotated[UserQuery, Query()],
        current_user: CurrentUser = Depends(get_current_user())
) -> HttpResponse[PageResult]:
    user_page_result: PageResult = await user_service.get_user_by_page(
        user_query=user_query,
        current_user=current_user
    )
    return HttpResponse.success(user_page_result)


@user_router.get("/detail/{id}")
async def get_user_detail(
        id: int, current_user: CurrentUser
) -> HttpResponse[UserDetail]:
    user_detail: UserDetail = await user_service.get_user_detail(id=id, request=request)
    return HttpResponse.success(user_detail)


@user_router.get("/export-template")
async def export_template(current_user: CurrentUser) -> StreamingResponse:
    return await excel_util.export_excel(schema=UserCreate, file_name="user_import_tpl")


@user_router.get("/export")
async def export_user_page(
        current_user: CurrentUser, ids: list[int] = Query(...)
) -> StreamingResponse:
    return await user_service.export_user_page(ids=ids, request=request)


@user_router.post("/create")
async def create_user(
        user_create: UserCreate, current_user: CurrentUser
) -> HttpResponse[int]:
    user: UserModel = await user_service.create_user(user_create=user_create, request=request)
    return HttpResponse.success(user.id)


@user_router.post("/batch-create")
async def batch_create_user(
        user_create_list: List[UserCreate], current_user: CurrentUser
) -> HttpResponse[List[int]]:
    ids: List[int] = await user_service.batch_create_user(user_create_list=user_create_list, request=request)
    return HttpResponse.success(ids)


@user_router.post("/import")
async def import_user(
        current_user: CurrentUser, file: UploadFile = Form()
) -> HttpResponse[List[UserCreate]]:
    user_create_list: List[UserCreate] = await user_service.import_user(file=file, request=request)
    return HttpResponse.success(user_create_list)


@user_router.delete("/remove/{id}")
async def remove(
        id: int, current_user: CurrentUser
) -> HttpResponse:
    await user_service.remove_by_id(id=id)
    return HttpResponse.success()


@user_router.delete("/batch-remove")
async def batch_remove(
        current_user: CurrentUser, ids: List[int] = Query(...),
) -> HttpResponse:
    await user_service.batch_remove_by_ids(ids=ids)
    return HttpResponse.success()


@user_router.put("/modify")
async def modify(
        user_modify: UserModify, current_user: CurrentUser
) -> HttpResponse:
    await user_service.modify_by_id(data=UserModel(**user_modify.model_dump(exclude_unset=True)))
    return HttpResponse.success()


@user_router.put("/batch-modify")
async def batch_modify(user_batch_modify: UserBatchModify, current_user: CurrentUser) -> HttpResponse:
    cleaned_data = {k: v for k, v in user_batch_modify.model_dump().items() if v is not None and k != "ids"}
    if len(cleaned_data) == 0:
        return HttpResponse.fail("内容不能为空")
    await user_service.batch_modify_by_ids(ids=user_batch_modify.ids, data=cleaned_data)
    return HttpResponse.success()
