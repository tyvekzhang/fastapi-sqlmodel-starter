"""BaseMapper defines the implemented functionalities"""

from abc import ABC, abstractmethod
from typing import Any, List


class BaseMapper(ABC):
    @abstractmethod
    async def insert(self, *, data: Any, db_session: Any) -> Any: ...

    @abstractmethod
    async def insert_batch(self, *, data_list: List[Any], db_session: Any) -> int: ...

    @abstractmethod
    async def select_by_id(self, *, id: Any, db_session: Any) -> Any: ...

    @abstractmethod
    async def select_count(self, *, db_session: Any) -> int: ...

    @abstractmethod
    async def select_list(
        self, *, page: int, size: int, db_session: Any, **kwargs
    ) -> List[Any]: ...

    @abstractmethod
    async def select_list_ordered(
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
    async def select_page(self, *, params: Any, db_session: Any) -> List[Any]: ...

    @abstractmethod
    async def select_page_ordered(
        self,
        *,
        params: Any,
        order_by: Any,
        sort_order: Any,
        db_session: Any,
    ) -> List[Any]: ...

    @abstractmethod
    async def update_by_id(self, *, data: Any, db_session: Any) -> int: ...

    @abstractmethod
    async def update_batch_by_ids(
        self, *, ids: List[Any], data: dict, db_session: Any = None
    ) -> int: ...

    @abstractmethod
    async def delete_by_id(self, *, id: Any, db_session: Any) -> int: ...

    @abstractmethod
    async def delete_batch_by_ids(self, *, ids: List[Any], db_session: Any) -> int: ...
