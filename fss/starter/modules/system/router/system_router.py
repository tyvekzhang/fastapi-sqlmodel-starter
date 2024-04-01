from fastapi import APIRouter

from fss.starter.modules.system.api.v1.probe.probe_api import router as probe_router

system_router = APIRouter()
system_router.include_router(probe_router, tags=["probe"], prefix="/probe")
