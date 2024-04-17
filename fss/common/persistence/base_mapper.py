"""BaseMapper defines the implemented functionalities"""

from abc import abstractmethod
from typing import Any, List

from fss.common.persistence.mapper import Mapper


class BaseMapper(Mapper):
    @abstractmethod
    async def insert(self, *, data: Any, db_session: Any) -> int:
        raise NotImplementedError

    @abstractmethod
    async def insert_batch(self, *, data_list: List[Any], db_session: Any) -> int:
        raise NotImplementedError

    @abstractmethod
    async def select_by_id(self, *, id: Any, db_session: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def select_count(self, *, db_session: Any) -> int:
        raise NotImplementedError

    @abstractmethod
    async def select_list(
        self, *, page: int, size: int, query: Any, db_session: Any
    ) -> List[Any]:
        raise NotImplementedError

    @abstractmethod
    async def select_list_ordered(
        self,
        *,
        page: int,
        size: int,
        query: Any,
        order_by: Any,
        sort_order: Any,
        db_session: Any,
    ) -> List[Any]:
        raise NotImplementedError

    @abstractmethod
    async def select_list_page(
        self, *, params: Any, query: Any, db_session: Any
    ) -> List[Any]:
        raise NotImplementedError

    @abstractmethod
    async def select_list_page_ordered(
        self,
        *,
        params: Any,
        query: Any,
        order_by: Any,
        sort_order: Any,
        db_session: Any,
    ) -> List[Any]:
        raise NotImplementedError

    @abstractmethod
    async def update_by_id(self, *, data: Any, db_session: Any) -> int:
        raise NotImplementedError

    @abstractmethod
    async def update_batch_by_ids(
        self, *, data_list: List[Any], db_session: Any
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    async def delete_by_id(self, *, id: Any, db_session: Any) -> int:
        raise NotImplementedError

    @abstractmethod
    async def delete_batch_by_ids(self, *, ids: List[Any], db_session: Any) -> int:
        raise NotImplementedError
