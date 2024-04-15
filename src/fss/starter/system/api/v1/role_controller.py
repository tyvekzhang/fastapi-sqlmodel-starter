"""Role operation controller"""

from fastapi import APIRouter, Depends

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
    Create role
    """
    role: RoleDO = await role_service.save(data=create_data)
    return result.success(data=role.id)
