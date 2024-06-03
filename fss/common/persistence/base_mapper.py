"""BaseMapper defines the database operations to be implemented"""

from abc import ABC, abstractmethod
from typing import Any, List


class BaseMapper(ABC):
    @abstractmethod
    async def insert_record(self, *, record: Any, db_session: Any) -> Any: ...

    @abstractmethod
    async def batch_insert_records(
        self, *, records: List[Any], db_session: Any
    ) -> int: ...

    @abstractmethod
    async def select_record_by_id(self, *, id: Any, db_session: Any) -> Any: ...

    @abstractmethod
    async def select_records(
        self, *, page: int, size: int, db_session: Any, **kwargs
    ) -> List[Any]: ...

    @abstractmethod
    async def select_ordered_records(
        self,
        *,
        page: int,
        size: int,
        order_by: Any,
        sort_order: Any,
        db_session: Any,
        **kwargs,
    ) -> List[Any]: ...

    @abstractmethod
    async def update_record_by_id(self, *, record: Any, db_session: Any) -> int: ...

    @abstractmethod
    async def batch_update_records_by_ids(
        self, *, ids: List[Any], record: dict, db_session: Any = None
    ) -> int: ...

    @abstractmethod
    async def delete_record_by_id(self, *, id: Any, db_session: Any) -> int: ...

    @abstractmethod
    async def batch_delete_records_by_ids(
        self, *, ids: List[Any], db_session: Any
    ) -> int: ...
