"""Abstract Service used in the project"""

from abc import ABC, abstractmethod
from typing import Any, List, TypeVar, Generic

T = TypeVar("T", bound=Any)
DEFAULT_BATCH_SIZE: int = 1000


class Service(Generic[T], ABC):
    @abstractmethod
    async def save(self, *, data: T) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def save_or_update(self, *, data: T) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def save_batch(self, *, data_list: List[T]) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def save_or_update_batch(self, *, data_list: List[T]) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, *, id: T) -> T:
        raise NotImplementedError

    @abstractmethod
    async def get_by_ids(self, *, ids: List[T], batch_size: int) -> List[Any]:
        raise NotImplementedError

    @abstractmethod
    async def count(
        self,
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    async def list(self, *, page: int, size: int, query: T) -> List[T]:
        raise NotImplementedError

    @abstractmethod
    async def list_ordered(
        self, *, page: int, size: int, query: T, order_by: T, sort_order: T
    ) -> List[T]:
        raise NotImplementedError

    @abstractmethod
    async def list_page(self, *, params: T, query: T) -> List[T]:
        raise NotImplementedError

    @abstractmethod
    async def list_page_ordered(self, *, params: T, query: T, sort_order: T) -> List[T]:
        raise NotImplementedError

    @abstractmethod
    async def update_by_id(self, *, data: T) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def update_batch_by_ids(self, *, data_list: List[T]) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def remove_by_id(self, *, id: T) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def remove_batch_by_ids(self, *, ids: List[Any]) -> bool:
        raise NotImplementedError
