"""Routing of system modules"""

from fastapi import APIRouter

from src.main.app.controller.v1.probe_controller import probe_router
from src.main.app.controller.v1.user_controller import user_router
from src.main.app.controller.v1.role_controller import role_router


def create_router() -> APIRouter:
    router = APIRouter()
    router.include_router(probe_router, tags=["probe"], prefix="/probe")
    router.include_router(user_router, tags=["user"], prefix="/user")
    router.include_router(role_router, tags=["role"], prefix="/role")

    return router
