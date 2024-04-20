"""User operation controller"""

from typing import List, Dict

from fastapi import APIRouter, Depends, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_pagination import Params
from starlette.responses import StreamingResponse

from fss.common.result import result
from fss.common.result.result import BaseResponse
from fss.common.schema.schema import Token, CurrentUser
from fss.common.security.security import get_current_user
from fss.common.security.security import get_password_hash
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
    Registers a new user with the provided credentials.

    Args:
        create_data: Data required for registration.

        user_service: Service handling user operations.
    Returns:
        BaseResponse with new user's ID.
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
    Retrieves the profile of the current user.

    Args:
        user_service: Service handling user operations.

        current_user: Currently authenticated user.
    Returns:
        BaseResponse with current user's profile information.
    """
    user: UserQuery = await user_service.find_by_id(id=current_user.user_id)
    return result.success(data=user)


@user_router.post("/login")
async def login(
    login_form: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service),
) -> Token:
    """
    Authenticates user and provides an access token.

    Args:
        login_form: Login credentials.

        user_service: Service handling user operations.
    Returns:
        Token object with access token.
    """
    loginCmd = LoginCmd(username=login_form.username, password=login_form.password)
    return await user_service.login(loginCmd)


@user_router.delete("/{id}")
async def remove_user(
    id: int,
    user_service: UserService = Depends(get_user_service),
    current_user: CurrentUser = Depends(get_current_user()),
) -> Dict:
    """
    Endpoint to remove a user by their ID.

    Args:
        id: User ID to remove.

        user_service: Service handling user operations.

        current_user: Logged-in user performing the operation.
    Returns:
        Success result message
    """
    await user_service.remove_by_id(id=id)
    return result.success()


@user_router.put("/")
async def update_user(
    updateUserCmd: UpdateUserCmd,
    user_service: UserService = Depends(get_user_service),
    current_user: CurrentUser = Depends(get_current_user()),
) -> Dict:
    """
    Endpoint to update user information.

    Args:
        updateUserCmd: Command containing updated user info.

        user_service: Service handling user operations.

        current_user: Logged-in user performing the operation.
    Returns:
        Success result message
    """
    await user_service.update_by_id(data=updateUserCmd)
    return result.success()


@user_router.get("/exportTemplate")
async def export_user_template(
    user_service: UserService = Depends(get_user_service),
    current_user: CurrentUser = Depends(get_current_user()),
) -> StreamingResponse:
    """
    Endpoint to export a template for user information.

    Args:
        user_service: Service for user operations.

        current_user: Logged-in user requesting the template.
    Returns:
        StreamingResponse with user field
    """
    return await user_service.export_user_template()


@user_router.post("/import")
async def import_user(
    file: UploadFile,
    user_service: UserService = Depends(get_user_service),
    current_user: CurrentUser = Depends(get_current_user()),
) -> Dict:
    """
    Endpoint to import user information from a file.

    Args:
        file: The file containing user information to import.

        user_service: Service handling user operations.

        current_user: Logged-in user performing the import.
    Returns:
        Success result message
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
    Endpoint to export user information based on provided parameters.

    Args:
        params: Filtering and format parameters for export.

        user_service: Service handling user operations.

        current_user: Logged-in user requesting the export.
    Returns:
        StreamingResponse with user info
    """
    return await user_service.export_user(params)


@user_router.get("/list")
async def list_user(
    page: int = 1,
    size: int = 100,
    user_service: UserService = Depends(get_user_service),
    current_user: CurrentUser = Depends(get_current_user()),
) -> BaseResponse[List[UserQuery]]:
    """
    Endpoint to list users with pagination.

    Args:
        page: The number of the current page.

        size: The number of items per page.

        user_service: Service handling user operations.

        current_user: Logged-in user performing the operation.
    Returns:
        BaseResponse with userQuery list.
    """
    results: List[UserQuery] = await user_service.list_user(page=page, size=size)
    return result.success(data=results)


@user_router.get("/count")
async def user_count(
    user_service: UserService = Depends(get_user_service),
    current_user: CurrentUser = Depends(get_current_user()),
) -> BaseResponse[int]:
    """
    Endpoint to count the total number of users.

    Args:
        user_service: Service handling user operations.

        current_user: Logged-in user requesting the count.
    Returns:
        BaseResponse with user count.
    """
    return result.success(await user_service.count())


@user_router.post("/{user_id}/roles")
async def user_roles(
    user_id: int,
    role_ids: List[int],
    user_role_service: UserService = Depends(get_user_role_service),
    current_user: CurrentUser = Depends(get_current_user()),
) -> Dict:
    """
    Endpoint to assign roles to a user.

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
    await user_role_service.save_batch(data_list=user_role_list)
    return result.success()
