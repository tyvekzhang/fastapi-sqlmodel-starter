from fastapi import APIRouter

router = APIRouter()


@router.get("/liveness")
def liveness():
    return {"code": 0, "msg": "hi"}


@router.get("/readiness")
async def readiness():
    return {"code": 0, "msg": "hello"}
