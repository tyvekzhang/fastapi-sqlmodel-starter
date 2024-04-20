"""Common service impl"""

from typing import Any, TypeVar, List, Generic, Type

from fss.common.persistence.base_mapper import BaseMapper
from fss.common.service.service import Service
from fss.starter.system.enum.system import SystemResponseCode
from fss.starter.system.exception.system import SystemException

T = TypeVar("T", bound=Any)
M = TypeVar("M", bound=BaseMapper)


class ServiceImpl(Generic[M, T], Service[T]):
    def __init__(self, mapper: Type[M]):
        self.mapper = mapper

    async def save(self, *, data: T) -> T:
        return await self.mapper.insert(data=data)

    async def save_batch(self, *, data_list: List[T]) -> bool:
        await self.mapper.insert_batch(data_list=data_list)
        return True

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
        affect_row: int = await self.mapper.update_by_id(data=data)
        if affect_row != 1:
            raise SystemException(
                SystemResponseCode.PARAMETER_ERROR.code,
                SystemResponseCode.PARAMETER_ERROR.msg,
            )
        return True

    async def update_batch_by_ids(
        self, *, ids: List[Any], data: dict, db_session: Any = None
    ) -> bool:
        affect_row: int = await self.mapper.update_batch_by_ids(ids=ids, data=data)
        if len(ids) != affect_row:
            raise SystemException(
                SystemResponseCode.PARAMETER_ERROR.code,
                SystemResponseCode.PARAMETER_ERROR.msg,
            )
        return True

    async def remove_by_id(self, *, id: T) -> bool:
        affect_row: int = await self.mapper.delete_by_id(id=id)
        if affect_row != 1:
            raise SystemException(
                SystemResponseCode.PARAMETER_ERROR.code,
                SystemResponseCode.PARAMETER_ERROR.msg,
            )
        return True

    async def remove_batch_by_ids(self, *, ids: List[Any]) -> bool:
        affect_row: int = await self.mapper.delete_batch_by_ids(ids=ids)
        if len(ids) != affect_row:
            raise SystemException(
                SystemResponseCode.PARAMETER_ERROR.code,
                SystemResponseCode.PARAMETER_ERROR.msg,
            )
        return True
