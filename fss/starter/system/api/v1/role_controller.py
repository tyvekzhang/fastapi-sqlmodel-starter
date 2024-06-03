"""Role operation controller"""

from typing import List, Dict

from fastapi import APIRouter, Depends

from fss.common.result import result
from fss.common.result.result import BaseResponse
from fss.common.schema.schema import CurrentUser
from fss.common.security.security import get_current_user
from fss.starter.system.factory.service_factory import get_role_service
from fss.starter.system.model.role_do import RoleDO
from fss.starter.system.schema.role_schema import RoleCreateCmd, RoleDeleteCmd
from fss.starter.system.service.role_service import RoleService

role_router = APIRouter()
role_service: RoleService = get_role_service()


@role_router.post("/")
async def create_role(
    role_create_cmd: RoleCreateCmd,
    current_user: CurrentUser = Depends(get_current_user()),
) -> BaseResponse[int]:
    """
    Creates a new role with the provided data.

    Args:
        role_create_cmd: Command with role creation data.
        current_user: Current user performing the action.

    Returns:
        BaseResponse with created role ID.
    """
    role: RoleDO = await role_service.save(record=role_create_cmd)
    return result.success(data=role.id)


@role_router.get("/rolesOrdered")
async def retrieve_ordered_roles(
    page: int = 1,
    size: int = 100,
    current_user: CurrentUser = Depends(get_current_user()),
) -> BaseResponse[List[RoleDO]]:
    """
    Retrieves a list of roles in an ordered manner.

    Args:
        page: Page number for listing roles.
        size: The size of the role list per page.
        current_user: Current user performing the action.

    Returns:
        BaseResponse with list of RoleDO.
    """
    results, _ = await role_service.retrieve_ordered_records(
        page=page, size=size, order_by="sort"
    )
    return result.success(data=results)


@role_router.get("/{id}")
async def get_role(
    id: int,
    current_user: CurrentUser = Depends(get_current_user()),
) -> BaseResponse[RoleDO]:
    """
    Retrieves a role by its ID.

    Args:
        id: The unique identifier of the role.
        current_user: Current user performing the action.

    Returns:
        BaseResponse with RoleDO details.
    """
    role_do: RoleDO = await role_service.retrieve_by_id(id=id)
    return result.success(data=role_do)


@role_router.post("/roles")
async def remove_role_by_ids(
    roleDeleteCmd: RoleDeleteCmd,
    current_user: CurrentUser = Depends(get_current_user()),
) -> Dict:
    """
    Delete roles by a list of IDs.

    Args:
        roleDeleteCmd: List of role IDs to delete.
        current_user: Current user performing the action.

    Returns:
        BaseResponse with count of deleted roles.
    """
    await role_service.remove_batch_by_ids(ids=roleDeleteCmd.role_ids)
    return result.success()
