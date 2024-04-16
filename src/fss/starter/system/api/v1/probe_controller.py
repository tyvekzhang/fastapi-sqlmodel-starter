"""Project health probe"""

from fastapi import APIRouter, Depends
from loguru import logger

from fss.common.cache.cache import get_cache_client, Cache
from fss.starter.system.enum.system import SystemResponseCode
from fss.starter.system.service.impl.user_service_impl import get_user_service
from fss.starter.system.service.user_service import UserService

probe_router = APIRouter()

USER_ID = 1
HI = "hi"
HELLO = "hello"


@probe_router.get("/liveness")
def liveness():
    """
    Liveness probe
    """
    return {"code": SystemResponseCode.SUCCESS.code, "msg": HI}


@probe_router.get("/readiness")
async def readiness(user_service: UserService = Depends(get_user_service)):
    """
    Readiness probe
    """
    try:
        cache_client: Cache = await get_cache_client()
        await cache_client.set(f"user:{USER_ID}", "ok")
        res = await cache_client.get(f"user:{USER_ID}")
        if "ok" != res:
            raise
        await cache_client.delete(f"user:{USER_ID}")
        await user_service.find_by_id(id=USER_ID)
    except Exception as e:
        logger.error(f"readiness error: {e}")
        return {
            "code": SystemResponseCode.SERVICE_INTERNAL_ERROR.code,
            "msg": SystemResponseCode.SERVICE_INTERNAL_ERROR.msg,
        }
    return {"code": SystemResponseCode.SUCCESS.code, "msg": HELLO}
