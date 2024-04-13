"""User operation controller"""

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
from fss.starter.system.schema.user_schema import (
    UserCreateCmd,
    UserQuery,
    LoginCmd,
    UpdateUserCmd,
)
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
    user: UserDO = await user_service.save(data=create_data)
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
