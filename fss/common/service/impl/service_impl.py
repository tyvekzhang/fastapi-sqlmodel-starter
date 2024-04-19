"""Common service impl"""

from typing import Any, TypeVar, List, Generic, Type

from fss.common.persistence.base_mapper import BaseMapper
from fss.common.service.service import Service

T = TypeVar("T", bound=Any)
M = TypeVar("M", bound=BaseMapper)


class ServiceImpl(Generic[M, T], Service[T]):
    def __init__(self, mapper: Type[M]):
        self.mapper = mapper

    async def save(self, *, data: T) -> T:
        result = await self.mapper.insert(data=data)
        return result

    async def save_batch(self, *, data_list: List[T]) -> int:
        result = await self.mapper.insert_batch(data_list=data_list)
        return result

    async def get_by_id(self, *, id: T) -> T:
        return await self.mapper.select_by_id(id=id)

    async def count(self) -> int:
        return await self.mapper.select_count()

    async def list(self, *, page: int, size: int, **kwargs) -> List[T]:
        return await self.mapper.select_list(page=page, size=size, **kwargs)

    async def list_ordered(
        self,
        *,
        page: int,
        size: int,
        order_by: T = None,
        sort_order: T = None,
        **kwargs,
    ) -> List[T]:
        return await self.mapper.select_list_ordered(
            page=page, size=size, order_by=order_by, sort_order=sort_order, **kwargs
        )

    async def list_page(self, *, params: T) -> List[T]:
        return await self.mapper.select_page(params=params)

    async def list_page_ordered(self, *, params: T = None) -> List[T]:
        return await self.mapper.select_page_ordered(params=params)

    async def update_by_id(self, *, data: T) -> bool:
        return await self.mapper.update_by_id(data=data)

    async def update_batch_by_ids(
        self, *, ids: List[Any], data: dict, db_session: Any = None
    ) -> int:
        return await self.mapper.update_batch_by_ids(ids=ids, data=data)

    async def remove_by_id(self, *, id: T) -> bool:
        return await self.mapper.delete_by_id(id=id)

    async def remove_batch_by_ids(self, *, ids: List[Any]) -> bool:
        return await self.mapper.delete_batch_by_ids(ids=ids)
