"""User operation controller"""

import json
from typing import List, Dict, Optional

from fastapi import APIRouter, Depends, UploadFile, Query
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_pagination import Params
from starlette.responses import StreamingResponse

from fss.common.result import result
from fss.common.result.result import BaseResponse
from fss.common.schema.schema import Token, CurrentUser
from fss.common.security.security import get_current_user
from fss.starter.system.factory.service_factory import get_user_service
from fss.starter.system.model.user_do import UserDO
from fss.starter.system.model.user_role_do import UserRoleDO
from fss.starter.system.schema.user_schema import (
    UserCreateCmd,
    UserQuery,
    LoginCmd,
    UpdateUserCmd,
)
from fss.starter.system.service.impl.user_role_service_impl import get_user_role_service
from fss.starter.system.service.user_service import UserService

user_router = APIRouter()
user_service: UserService = get_user_service()


@user_router.post("/register")
async def register_user(
    user_create_cmd: UserCreateCmd,
) -> BaseResponse[int]:
    """
    Registers a new user.

    Args:
        user_create_cmd: Data required for registration.

    Returns:
        BaseResponse with new user's ID.
    """
    user: UserDO = await user_service.register(user_create_cmd=user_create_cmd)
    return result.success(data=user.id)


@user_router.post("/login")
async def login(
    login_form: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    """
    Authenticates user and provides an access token.

    Args:
        login_form: Login credentials.

    Returns:
        Token object with access token.
    """
    login_cmd = LoginCmd(username=login_form.username, password=login_form.password)
    return await user_service.login(login_cmd=login_cmd)


@user_router.get("/me")
async def get_user(
    current_user: CurrentUser = Depends(get_current_user()),
) -> BaseResponse[UserQuery]:
    """
    Retrieves the profile of the current user.

    Args:
        current_user: Currently authenticated user.

    Returns:
        BaseResponse with current user's profile information.
    """
    user: UserQuery = await user_service.find_by_id(id=current_user.user_id)
    return result.success(data=user)


@user_router.delete("/{id}")
async def delete_user(
    id: int,
    current_user: CurrentUser = Depends(get_current_user()),
) -> Dict:
    """
    Remove a user by their ID.

    Args:
        id: User ID to remove.
        current_user: Logged-in user performing the operation.

    Returns:
        Success result message
    """
    await user_service.remove_by_id(id=id)
    return result.success()


@user_router.put("/")
async def update_user(
    update_user_cmd: UpdateUserCmd,
    current_user: CurrentUser = Depends(get_current_user()),
) -> Dict:
    """
    Update user information.

    Args:
        update_user_cmd: Command containing updated user info.
        current_user: Logged-in user performing the operation.

    Returns:
        Success result message
    """
    await user_service.modify_by_id(update_user_cmd=update_user_cmd)
    return result.success()


@user_router.get("/exportTemplate")
async def export_user_template(
    current_user: CurrentUser = Depends(get_current_user()),
) -> StreamingResponse:
    """
    Export a template for user information.

    Args:
        current_user: Logged-in user requesting the template.

    Returns:
        StreamingResponse with user field
    """
    return await user_service.export_user_template()


@user_router.post("/import")
async def import_user(
    file: UploadFile,
    current_user: CurrentUser = Depends(get_current_user()),
) -> Dict:
    """
    Import user information from a file.

    Args:
        file: The file containing user information to import.

        current_user: Logged-in user performing the import.
    Returns:
        Success result message
    """
    await user_service.import_user(file=file)
    return result.success()


@user_router.get("/export")
async def export_user(
    params: Params = Depends(),
    current_user: CurrentUser = Depends(get_current_user()),
) -> StreamingResponse:
    """
    Export user information based on provided parameters.

    Args:
        params: Filtering and format parameters for export.

        current_user: Logged-in user requesting the export.

    Returns:
        StreamingResponse with user info
    """
    return await user_service.export_user(params=params)


@user_router.get("/list")
async def list_user(
    page: int = Query(1, description="The number of the current page."),
    size: int = Query(100, description="The number of items per page."),
    filter_by: Optional[str] = Query(
        None,
        description="Filter criteria in JSON format.",
        example={"nickname": "string"},
    ),
    like: Optional[str] = Query(
        None,
        description="Like criteria in JSON format.",
        example={"username": "str%"},
    ),
    current_user: CurrentUser = Depends(get_current_user),
) -> BaseResponse:
    """
    List users with pagination.

    Args:
        page: The number of the current page.

        size: The number of items per page.

        filter_by: Filter criteria in JSON format.

        like: Like criteria in JSON format.

        current_user: Logged-in user performing the operation.

    Returns:
        BaseResponse with userQuery list.
    """
    filter_by_dict = json.loads(filter_by) if filter_by else None
    like_dict = json.loads(like) if like else None

    records: List[UserQuery] = await user_service.retrieve_user(
        page=page, size=size, filter_by=filter_by_dict, like=like_dict
    )
    return BaseResponse(data=records)


@user_router.post("/{user_id}/roles")
async def user_roles(
    user_id: int,
    role_ids: List[int],
    user_role_service: UserService = Depends(get_user_role_service),
    current_user: CurrentUser = Depends(get_current_user()),
) -> Dict:
    """
    Assign roles to a user.

    Args:
        user_id: ID of the user to assign roles to.
        role_ids: List of role IDs to assign to the user.
        user_role_service: Service handling user-role associations.
        current_user: Logged-in user performing the role assignment.
    Returns:
        Success result message
    """
    user_role_list = []
    for i, role_id in enumerate(role_ids):
        manual_id = user_id + role_id + i
        user_role_list.append(
            UserRoleDO(id=manual_id, user_id=user_id, role_id=role_id)
        )
    await user_role_service.batch_save(records=user_role_list)
    return result.success()
