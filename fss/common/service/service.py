"""Abstract Service used in the project"""

from abc import ABC, abstractmethod
from typing import Any, List, TypeVar, Generic, Tuple

T = TypeVar("T", bound=Any)


class Service(Generic[T], ABC):
    @abstractmethod
    async def save(self, *, record: T) -> T: ...

    @abstractmethod
    async def batch_save(self, *, records: List[T]) -> bool: ...

    @abstractmethod
    async def retrieve_by_id(self, *, id: T) -> T: ...

    @abstractmethod
    async def retrieve_by_ids(self, *, ids: List[T]) -> List[T]: ...

    @abstractmethod
    async def retrieve_records(
        self, *, page: int, size: int, **kwargs
    ) -> Tuple[
        List[Any],
        int,
    ]: ...

    @abstractmethod
    async def retrieve_ordered_records(
        self, *, page: int, size: int, order_by: T, sort_order: T, **kwargs
    ) -> Tuple[
        List[Any],
        int,
    ]: ...

    @abstractmethod
    async def modify_by_id(self, *, update_user_cmd: T) -> bool: ...

    @abstractmethod
    async def batch_modify_by_ids(
        self, *, ids: List[Any], record: dict, db_session: Any = None
    ) -> bool: ...

    @abstractmethod
    async def remove_by_id(self, *, id: T) -> bool: ...

    @abstractmethod
    async def batch_remove_by_ids(self, *, ids: List[Any]) -> bool: ...
