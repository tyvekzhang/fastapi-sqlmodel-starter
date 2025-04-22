"""BaseMapper defines the database operations to be implemented"""

from abc import ABC, abstractmethod
from typing import Any, List, Tuple


class MapperBase(ABC):
    @abstractmethod
    async def insert(self, *, record: Any, db_session: Any = None) -> Any: ...

    @abstractmethod
    async def batch_insert(self, *, records: List[Any], db_session: Any = None) -> int: ...

    @abstractmethod
    async def select_by_id(self, *, id: Any, db_session: Any = None) -> Any: ...

    @abstractmethod
    async def select_by_ids(self, *, ids: List[Any], db_session: Any = None) -> List[Any]: ...

    @abstractmethod
    async def select_by_page(
        self, *, current: int, size: int, db_session: Any = None, **kwargs
    ) -> Tuple[
        List[Any],
        int,
    ]: ...

    @abstractmethod
    async def select_by_ordered_page(
        self,
        *,
        current: int,
        pageSize: int,
        order_by: Any,
        sort_order: Any,
        db_session: Any = None,
        **kwargs,
    ) -> Tuple[
        List[Any],
        int,
    ]: ...

    @abstractmethod
    async def update_by_id(self, *, record: Any, db_session: Any = None) -> int: ...

    @abstractmethod
    async def batch_update_by_ids(self, *, ids: List[Any], record: dict, db_session: Any = None) -> int: ...

    @abstractmethod
    async def delete_by_id(self, *, id: Any, db_session: Any = None) -> int: ...

    @abstractmethod
    async def batch_delete_by_ids(self, *, ids: List[Any], db_session: Any = None) -> int: ...
