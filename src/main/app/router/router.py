"""Routing of system modules"""

from fastapi import APIRouter

from src.main.app.controller.probe_controller import probe_router
from src.main.app.controller.user_controller import user_router


def create_router() -> APIRouter:
    router = APIRouter()
    router.include_router(probe_router, tags=["probe"], prefix="/probe")
    router.include_router(user_router, tags=["user"], prefix="/user")

    return router
