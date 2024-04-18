"""Role operation controller"""

from typing import Any, List

from fastapi import APIRouter, Depends
from fastapi_pagination import Params

from fss.common.result import result
from fss.common.result.result import BaseResponse
from fss.common.schema.schema import CurrentUser
from fss.common.security.security import get_current_user
from fss.starter.system.model.role_do import RoleDO
from fss.starter.system.schema.role_schema import RoleCreateCmd
from fss.starter.system.service.impl.role_service_impl import get_role_service
from fss.starter.system.service.role_service import RoleService

role_router = APIRouter()


@role_router.post("/")
async def create_role(
    create_data: RoleCreateCmd,
    role_service: RoleService = Depends(get_role_service),
    current_user: CurrentUser = Depends(get_current_user()),
) -> BaseResponse[int]:
    """
    Creates a new role with the provided data.

    Args:
        create_data: Command with role creation data.

        role_service: Service handling role-related operations.

        current_user: Current user performing the action.
    Returns:
        BaseResponse with created role ID.
    """
    role: RoleDO = await role_service.save(data=create_data)
    return result.success(data=role.id)


@role_router.get("/listOrdered")
async def list_ordered_role(
    page: int = 1,
    size: int = 100,
    query: Any = None,
    role_service: RoleService = Depends(get_role_service),
    current_user: CurrentUser = Depends(get_current_user()),
) -> BaseResponse[List[RoleDO]]:
    """
    Retrieves a list of roles in an ordered manner.

    Args:
        page: Page number for listing roles.

        size: The size of the role list per page.

        query: Query parameter for filtering roles.

        role_service: Service handling role-related operations.

        current_user: Current user performing the action.
    Returns:
        BaseResponse with list of RoleDO.
    """
    results: List[RoleDO] = await role_service.list_ordered(
        page=page, size=size, query=query, order_by="sort"
    )
    return result.success(data=results)


@role_router.get("/pageOrdered")
async def list_page_ordered_role(
    params: Params = Depends(),
    role_service: RoleService = Depends(get_role_service),
    current_user: CurrentUser = Depends(get_current_user()),
) -> Any:
    """
    Retrieves paginated roles in an ordered manner.

    Args:
        params: Pagination and ordering parameters.

        role_service: Service handling role-related operations.

        current_user: Current user performing the action.
    Returns:
        BaseResponse with paginated roles.
    """
    results = await role_service.list_page_ordered(params=params)
    return result.success(data=results)


@role_router.get("/{id}")
async def get_role(
    id: int,
    role_service: RoleService = Depends(get_role_service),
    current_user: CurrentUser = Depends(get_current_user()),
) -> BaseResponse[RoleDO]:
    """
    Retrieves a role by its ID.

    Args:
        id: The unique identifier of the role.

        role_service: Service handling role-related operations.

        current_user: Current user performing the action.
    Returns:
        BaseResponse with RoleDO details.
    """
    results = await role_service.get_by_id(id=id)
    return result.success(data=results)


@role_router.post("/roles")
async def remove_role_by_ids(
    role_ids: list[int],
    role_service: RoleService = Depends(get_role_service),
    current_user: CurrentUser = Depends(get_current_user()),
) -> BaseResponse[int]:
    """
    Deletes roles by a list of IDs.

    Args:
        role_ids: List of role IDs to delete.

        role_service: Service handling role-related operations.

        current_user: Current user performing the action.
    Returns:
        BaseResponse with count of deleted roles.
    """
    results = await role_service.remove_batch_by_ids(ids=role_ids)
    return result.success(data=results)
