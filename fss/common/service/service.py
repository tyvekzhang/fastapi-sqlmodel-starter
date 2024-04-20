"""Abstract Service used in the project"""

from abc import ABC, abstractmethod
from typing import Any, List, TypeVar, Generic

T = TypeVar("T", bound=Any)


class Service(Generic[T], ABC):
    @abstractmethod
    async def save(self, *, data: T) -> T: ...

    @abstractmethod
    async def save_batch(self, *, data_list: List[T]) -> bool: ...

    @abstractmethod
    async def get_by_id(self, *, id: T) -> T: ...

    @abstractmethod
    async def count(
        self,
    ) -> int: ...

    @abstractmethod
    async def list(self, *, page: int, size: int, **kwargs) -> List[T]: ...

    @abstractmethod
    async def list_ordered(
        self, *, page: int, size: int, order_by: T, sort_order: T, **kwargs
    ) -> List[T]: ...

    @abstractmethod
    async def list_page(self, *, params: T) -> List[T]: ...

    @abstractmethod
    async def list_page_ordered(self, *, params: T) -> List[T]: ...

    @abstractmethod
    async def update_by_id(self, *, data: T) -> bool: ...

    @abstractmethod
    async def update_batch_by_ids(
        self, *, ids: List[Any], data: dict, db_session: Any = None
    ) -> bool: ...

    @abstractmethod
    async def remove_by_id(self, *, id: T) -> bool: ...

    @abstractmethod
    async def remove_batch_by_ids(self, *, ids: List[Any]) -> bool: ...
