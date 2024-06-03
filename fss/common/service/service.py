"""Abstract Service used in the project"""

from abc import ABC, abstractmethod
from typing import Any, List, TypeVar, Generic

T = TypeVar("T", bound=Any)


class Service(Generic[T], ABC):
    @abstractmethod
    async def save(self, *, record: T) -> T: ...

    @abstractmethod
    async def batch_save(self, *, records: List[T]) -> bool: ...

    @abstractmethod
    async def retrieve_by_id(self, *, id: T) -> T: ...

    @abstractmethod
    async def retrieve_records(self, *, page: int, size: int, **kwargs) -> List[T]: ...

    @abstractmethod
    async def retrieve_ordered_records(
        self, *, page: int, size: int, order_by: T, sort_order: T, **kwargs
    ) -> List[T]: ...

    @abstractmethod
    async def edit_by_id(self, *, record: T) -> bool: ...

    @abstractmethod
    async def batch_edit_by_ids(
        self, *, ids: List[Any], record: dict, db_session: Any = None
    ) -> bool: ...

    @abstractmethod
    async def remove_by_id(self, *, id: T) -> bool: ...

    @abstractmethod
    async def remove_batch_by_ids(self, *, ids: List[Any]) -> bool: ...
