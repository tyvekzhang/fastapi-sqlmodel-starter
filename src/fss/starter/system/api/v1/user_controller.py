"""User operation controller"""

from typing import Any, List

from fastapi import APIRouter, Depends, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_pagination import Params
from starlette.responses import StreamingResponse

from fss.common.result import result
from fss.common.result.result import BaseResponse
from fss.common.schema.schema import Token, CurrentUser
from fss.common.security.security import get_current_user
from fss.common.util.security import get_password_hash
from fss.starter.system.model.user_do import UserDO
from fss.starter.system.model.user_role_do import UserRoleDO
from fss.starter.system.schema.user_schema import (
    UserCreateCmd,
    UserQuery,
    LoginCmd,
    UpdateUserCmd,
)
from fss.starter.system.service.impl.user_role_service_impl import get_user_role_service
from fss.starter.system.service.impl.user_service_impl import get_user_service
from fss.starter.system.service.user_service import UserService

user_router = APIRouter()


@user_router.post("/register")
async def register_user(
    create_data: UserCreateCmd, user_service: UserService = Depends(get_user_service)
) -> BaseResponse[int]:
    """
    User registration
    """
    create_data.password = await get_password_hash(create_data.password)
    user: UserDO = await user_service.register(data=create_data)
    return result.success(data=user.id)


@user_router.get("/me")
async def get_user(
    user_service: UserService = Depends(get_user_service),
    current_user: CurrentUser = Depends(get_current_user()),
) -> BaseResponse[UserQuery]:
    """
    Query user info
    """
    user: UserQuery = await user_service.find_by_id(id=current_user.user_id)
    return result.success(data=user)


@user_router.post("/login")
async def login(
    login_form: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service),
) -> Token:
    """
    User login
    """
    loginCmd = LoginCmd(username=login_form.username, password=login_form.password)
    return await user_service.login(loginCmd)


@user_router.delete("/{id}")
async def remove_user(
    id: int,
    user_service: UserService = Depends(get_user_service),
    current_user: CurrentUser = Depends(get_current_user()),
) -> None:
    """
    Remove user
    """
    await user_service.remove_by_id(id=id)
    return result.success()


@user_router.put("/")
async def update_user(
    updateUserCmd: UpdateUserCmd,
    user_service: UserService = Depends(get_user_service),
    current_user: CurrentUser = Depends(get_current_user()),
) -> None:
    """
    Update user
    """
    await user_service.update_by_id(data=updateUserCmd)
    return result.success()


@user_router.get("/exportTemplate")
async def export_user_template(
    user_service: UserService = Depends(get_user_service),
    current_user: CurrentUser = Depends(get_current_user()),
) -> StreamingResponse:
    """
    Export user template
    """
    return await user_service.export_user_template()


@user_router.post("/import")
async def import_user(
    file: UploadFile,
    user_service: UserService = Depends(get_user_service),
    current_user: CurrentUser = Depends(get_current_user()),
) -> None:
    """
    Import user info
    """
    await user_service.import_user(file)
    return result.success()


@user_router.get("/export")
async def export_user(
    params: Params = Depends(),
    user_service: UserService = Depends(get_user_service),
    current_user: CurrentUser = Depends(get_current_user()),
) -> StreamingResponse:
    """
    Export user info
    """
    return await user_service.export_user(params)


@user_router.get("/list")
async def list_user(
    page: int = 1,
    size: int = 100,
    query: Any = None,
    user_service: UserService = Depends(get_user_service),
    current_user: CurrentUser = Depends(get_current_user()),
) -> BaseResponse[List[UserQuery]]:
    """
    List user info
    """
    results: List[UserQuery] = await user_service.list_user(
        page=page, size=size, query=query
    )
    return result.success(data=results)


@user_router.get("/count")
async def user_count(
    user_service: UserService = Depends(get_user_service),
    current_user: CurrentUser = Depends(get_current_user()),
) -> BaseResponse[int]:
    """
    Counting the number of users
    """
    return result.success(await user_service.count())


@user_router.post("/{user_id}/roles")
async def user_roles(
    user_id: int,
    role_ids: List[int],
    user_role_service: UserService = Depends(get_user_role_service),
    current_user: CurrentUser = Depends(get_current_user()),
) -> BaseResponse[int]:
    """
    Assign roles to users
    """
    user_role_list = []
    for i, role_id in enumerate(role_ids):
        manual_id = user_id + role_id + i
        user_role_list.append(
            UserRoleDO(id=manual_id, user_id=user_id, role_id=role_id)
        )
    print(user_role_list)
    await user_role_service.save_batch(data_list=user_role_list)
    return result.success()
