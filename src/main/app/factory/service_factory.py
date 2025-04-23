"""Service factory to produces required services"""

from typing import Optional

from src.main.app.mapper.user_mapper import userMapper
from src.main.app.service.impl.user_service_impl import UserServiceImpl
from src.main.app.service.user_service import UserService

_singleton_user_service_instance: Optional[UserService] = None


def get_user_service(service_name: str = "default") -> UserService:
    """
    Return an instance of the UserService implementation.

    Returns:
        UserService: An instance of the UserServiceImpl class.
    """
    global _singleton_user_service_instance
    if service_name == "default":
        if _singleton_user_service_instance is None:
            _singleton_user_service_instance = UserServiceImpl(mapper=userMapper)
        return _singleton_user_service_instance
    else:
        raise ValueError(f"Unknown service name: {service_name}")
