"""User operation controller"""

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from fss.common.result import result
from fss.common.result.result import BaseResponse
from fss.common.schema.token import Token
from fss.common.security.security import oauth2_scheme
from fss.common.util.security import get_password_hash
from fss.starter.system.model.user_do import UserDO
from fss.starter.system.schema.user_schema import UserCreateCmd, UserQuery, LoginCmd
from fss.starter.system.service.impl.user_service_impl import get_user_service
from fss.starter.system.service.user_service import UserService

user_router = APIRouter()


# User registration
@user_router.post("/register")
async def create_user(
        create_data: UserCreateCmd, user_service: UserService = Depends(get_user_service)
) -> BaseResponse[int]:
    create_data.password = await get_password_hash(create_data.password)
    user: UserDO = await user_service.save(data=create_data)
    return result.success(data=user.id)


# Query user info
@user_router.get("/{id}")
async def get_user(
        id: int,
        user_service: UserService = Depends(get_user_service),
        token: str = Depends(oauth2_scheme)
) -> BaseResponse[UserQuery]:
    user: UserDO = await user_service.find_by_id(id=id)
    return result.success(data=user)


# User login
@user_router.post("/login")
async def login(
        login_form: OAuth2PasswordRequestForm = Depends(),
        user_service: UserService = Depends(get_user_service),
) -> BaseResponse[Token]:
    loginCmd = LoginCmd(username=login_form.username, password=login_form.password)
    token: Token = await user_service.login(loginCmd)
    return result.success(data=token)
