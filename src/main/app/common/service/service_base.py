"""Abstract Service used in the project"""

from abc import ABC, abstractmethod
from typing import Any, List, TypeVar, Generic, Tuple, Union, Dict

from sqlmodel import SQLModel

T = TypeVar("T", bound=SQLModel)


class ServiceBase(Generic[T], ABC):
    @abstractmethod
    async def save(self, *, data: T) -> T: ...

    @abstractmethod
    async def batch_save(self, *, data: List[T]) -> int: ...

    @abstractmethod
    async def retrieve_by_id(self, *, id: Union[int, str]) -> T: ...

    @abstractmethod
    async def retrieve_by_ids(self, *, ids: Union[List[int], List[str]]) -> List[T]: ...

    @abstractmethod
    async def retrieve_data(
        self, *, page: int, size: int, **kwargs
    ) -> Tuple[
        List[T],
        int,
    ]: ...

    @abstractmethod
    async def retrieve_ordered_data(
        self, *, page: int, size: int, order_by: str, sort_order: str, **kwargs
    ) -> Tuple[
        List[T],
        int,
    ]: ...

    @abstractmethod
    async def modify_by_id(self, *, data: T) -> None: ...

    @abstractmethod
    async def batch_modify_by_ids(
        self, *, ids: Union[List[int], List[str]], data: Dict, db_session: Any = None
    ) -> None: ...

    @abstractmethod
    async def remove_by_id(self, *, id: Union[int, str]) -> None: ...

    @abstractmethod
    async def batch_remove_by_ids(self, *, ids: Union[List[int], List[str]]) -> None: ...
