"""User operation controller"""

from typing import Annotated

from fastapi import APIRouter, Path, Depends

from fss.common.result import result
from fss.common.result.result import BaseResponse
from fss.common.util.security import get_password_hash
from fss.starter.system.schema.user_schema import UserCreate, UserQuery
from fss.starter.system.service.impl.user_service_impl import get_user_service
from fss.starter.system.service.user_service import UserService

user_router = APIRouter()


# User registration
@user_router.post("")
async def create_user(
    create_data: UserCreate, user_service: UserService = Depends(get_user_service)
) -> BaseResponse[int]:
    create_data.password = get_password_hash(create_data.password)
    res = await user_service.save(data=create_data)
    return result.success(data=res.id)


# Query user info
@user_router.get("/{id}")
async def get_user(
    id: Annotated[int, Path(title="The ID of the user to get")],
    user_service: UserService = Depends(get_user_service),
) -> BaseResponse[UserQuery]:
    res = await user_service.find_by_id(id=id)
    return result.success(data=res)
