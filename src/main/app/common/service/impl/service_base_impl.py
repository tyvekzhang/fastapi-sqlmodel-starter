"""Common service impl"""

from typing import Any, TypeVar, List, Generic, Tuple, Union, Dict

from src.main.app.common.entity.base_entity import BaseModel
from src.main.app.common.mapper.impl.mapper_base_impl import SqlModelMapper
from src.main.app.common.service.service_base import ServiceBase

T = TypeVar("T", bound=BaseModel)
M = TypeVar("M", bound=SqlModelMapper)


class ServiceBaseImpl(Generic[M, T], ServiceBase[T]):
    def __init__(self, mapper: M):
        self.mapper = mapper

    async def save(self, *, data: T) -> T:
        return await self.mapper.insert(record=data)

    async def batch_save(self, *, data: List[T]) -> int:
        return await self.mapper.batch_insert(records=data)

    async def retrieve_by_id(self, *, id: Union[int, str]) -> T:
        return await self.mapper.select_by_id(id=id)

    async def retrieve_by_ids(self, *, ids: Union[List[int], List[str]]) -> List[T]:
        return await self.mapper.select_by_ids(ids=ids)

    async def retrieve_data(
        self, *, page: int, size: int, **kwargs
    ) -> Tuple[
        List[T],
        int,
    ]:
        return await self.mapper.select_by_page(current=page, pageSize=size, **kwargs)

    async def retrieve_ordered_data(
        self, *, page: int, size: int, order_by: str, sort_order: str, **kwargs
    ) -> Tuple[
        List[T],
        int,
    ]:
        return await self.mapper.select_by_ordered_page(
            current=page, pageSize=size, order_by=order_by, sort_order=sort_order, **kwargs
        )

    async def modify_by_id(self, *, data: T) -> None:
        affect_row: int = await self.mapper.update_by_id(record=data)
        if affect_row != 1:
            raise ValueError

    async def batch_modify_by_ids(
        self, *, ids: Union[List[int], List[str]], data: Dict, db_session: Any = None
    ) -> None:
        affect_row: int = await self.mapper.batch_update_by_ids(ids=ids, record=data)
        if len(ids) != affect_row:
            raise ValueError

    async def remove_by_id(self, *, id: Union[int, str]) -> None:
        affect_row: int = await self.mapper.delete_by_id(id=id)
        if affect_row != 1:
            raise ValueError

    async def batch_remove_by_ids(self, *, ids: Union[List[int], List[str]]) -> None:
        affect_row: int = await self.mapper.batch_delete_by_ids(ids=ids)
        if len(ids) != affect_row:
            raise ValueError
