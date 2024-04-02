"""Routing of system modules"""

from fastapi import APIRouter

from fss.starter.system.api.v1.probe_controller import probe_router
from fss.starter.system.api.v1.user_controller import user_router

system_router = APIRouter()
system_router.include_router(probe_router, tags=["probe"], prefix="/probe")
system_router.include_router(user_router, tags=["user"], prefix="/user")
