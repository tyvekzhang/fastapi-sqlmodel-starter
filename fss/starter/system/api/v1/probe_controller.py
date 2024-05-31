"""Project health probe"""

from fastapi import APIRouter, Depends

from fss.common.cache.cache import get_cache_client, Cache
from fss.starter.system.enum.system import SystemResponseCode
from fss.starter.system.factory.service_factory import get_user_service
from fss.starter.system.service.user_service import UserService

probe_router = APIRouter()


@probe_router.get("/liveness")
async def liveness():
    """
    Check the system's live status.

    Returns:
        dict: A status object with a 'code' and a 'msg' indicating liveness.
    """
    return {"code": SystemResponseCode.SUCCESS.code, "msg": "Hi"}


@probe_router.get("/readiness")
async def readiness(
    user_id: int = 1, user_service: UserService = Depends(get_user_service)
):
    """
    Checks system and dependencies' readiness.

    Args:
        user_id (int, optional): ID for readiness check, defaults to 1.

        user_service (UserService, optional): Service for user-related operations.
    Returns:
        dict: Response with 'code' and 'msg' indicating readiness status.
    """
    try:
        cache_client: Cache = await get_cache_client()
        cache_key = f"user:{user_id}"
        await cache_client.set(cache_key, "Ok")
        res = await cache_client.get(cache_key)

        if "Ok" != res:
            raise ValueError("Cache read mismatch")

        await cache_client.delete(cache_key)
        await user_service.find_by_id(id=user_id)
    except Exception as e:
        return {
            "code": SystemResponseCode.SERVICE_INTERNAL_ERROR.code,
            "msg": f"Readiness check failed: {e}",
        }

    return {"code": SystemResponseCode.SUCCESS.code, "msg": "Hello"}
