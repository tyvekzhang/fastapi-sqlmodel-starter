from fastapi.security import OAuth2PasswordBearer

from fss.common.config import configs

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{configs.api_version}/user/login")
