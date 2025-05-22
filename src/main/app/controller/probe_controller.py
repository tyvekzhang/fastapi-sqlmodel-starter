"""Project health probe"""

from fastapi import APIRouter, Depends

from src.main.app.common.cache.cache import get_cache_client, Cache
from src.main.app.common.schema.response import HttpResponse
from src.main.app.enums.system import SystemResponseCode
from src.main.app.factory.service_factory import get_user_service
from src.main.app.service.user_service import UserService

probe_router = APIRouter()


@probe_router.get("/liveness")
async def liveness() -> HttpResponse[str]:
    """
    Check if the system is alive.

    Returns:
        HttpResponse[str]: An HTTP response containing a success message
        with the string "Hi" as data.
    """
    return HttpResponse.success(data="Hi")


@probe_router.get("/readiness")
async def readiness(user_id: int = 1, user_service: UserService = Depends(get_user_service)) -> HttpResponse[str]:
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
        return HttpResponse.fail(code=SystemResponseCode.SERVICE_INTERNAL_ERROR.code, msg=str(e))

    return HttpResponse.success(data="Hello")
