"""Common service impl"""

from typing import Any, TypeVar, List, Generic, Type

from fss.common.persistence.base_mapper import BaseMapper
from fss.common.service.service import Service

T = TypeVar("T", bound=Any)
M = TypeVar("M", bound=BaseMapper)


class ServiceImpl(Generic[M, T], Service[T]):
    def __init__(self, mapper: Type[M]):
        self.mapper = mapper

    async def save(self, *, data: T) -> bool:
        result = await self.mapper.insert(data=data)
        return result

    async def save_or_update(self, *, data: T) -> bool:
        if data.id is None:
            result = await self.mapper.insert(data=data)
        else:
            result = await self.update_by_id(data=data)
        return result

    async def save_batch(self, *, data_list: List[T]) -> bool:
        result = await self.mapper.insert_batch(data_list=data_list)
        return result == len(data_list)

    async def save_or_update_batch(self, *, data_list: List[T]) -> bool:
        if len(data_list) == 0:
            return False
        if data_list[0].id is None:
            return await self.save_batch(data_list=data_list)
        else:
            return await self.update_batch_by_ids(data_list=data_list)

    async def get_by_id(self, *, id: T) -> T:
        return await self.mapper.select_by_id(id=id)

    async def get_by_ids(self, *, ids: List[T], batch_size: int = 1000) -> List[Any]:
        return await self.mapper.select_by_ids(ids=ids, batch_size=batch_size)

    async def count(self) -> int:
        return await self.mapper.select_count()

    async def list(self, *, page: int, size: int, query: T) -> List[T]:
        return await self.mapper.select_list(page=page, size=size, query=query)

    async def list_ordered(
        self, *, page: int, size: int, query: T, order_by: T, sort_order: T
    ) -> List[T]:
        return await self.mapper.select_list_ordered(
            page=page, size=size, query=query, order_by=order_by, sort_order=sort_order
        )

    async def list_page(self, *, params: T, query: T) -> List[T]:
        return await self.mapper.select_list_page(params=params, query=query)

    async def list_page_ordered(self, *, params: T, query: T, sort_order: T) -> List[T]:
        return await self.mapper.select_list_page_ordered(
            params=params, query=query, sort_order=sort_order
        )

    async def update_by_id(self, *, data: T) -> bool:
        return await self.mapper.update_by_id(data=data)

    async def update_batch_by_ids(self, *, data_list: List[T]) -> bool:
        return await self.mapper.update_batch_by_ids(data_list=data_list)

    async def remove_by_id(self, *, id: T) -> bool:
        return await self.mapper.delete_by_id(id=id)

    async def remove_batch_by_ids(self, *, ids: List[Any]) -> bool:
        return await self.mapper.delete_batch_by_ids(ids=ids)
