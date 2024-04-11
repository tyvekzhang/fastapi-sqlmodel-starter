"""Project health probe"""

from fastapi import APIRouter, Depends
from loguru import logger

from fss.starter.system.enum.system import SystemResponseCode
from fss.starter.system.service.impl.user_service_impl import get_user_service
from fss.starter.system.service.user_service import UserService

probe_router = APIRouter()

USER_ID = 1
HI = "hi"
HELLO = "hello"


# Liveness probe
@probe_router.get("/liveness")
def liveness():
    return {"code": SystemResponseCode.SUCCESS.code, "msg": HI}


# Readiness probe
@probe_router.get("/readiness")
async def readiness(user_service: UserService = Depends(get_user_service)):
    try:
        await user_service.find_by_id(USER_ID)
    except Exception as e:
        logger.error(f"readiness error: {e}")
        return {
            "code": SystemResponseCode.SERVICE_INTERNAL_ERROR.code,
            "msg": SystemResponseCode.SERVICE_INTERNAL_ERROR.msg,
        }
    return {"code": SystemResponseCode.SUCCESS.code, "msg": HELLO}
