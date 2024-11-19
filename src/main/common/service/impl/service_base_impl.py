"""Common service impl"""

from typing import Any, TypeVar, List, Generic, Type, Tuple

from src.main.common.persistence.mapper_base import MapperBase
from src.main.common.service.service_base import ServiceBase
from src.main.system.enum.system import SystemResponseCode
from src.main.system.exception.system import SystemException

T = TypeVar("T", bound=Any)
M = TypeVar("M", bound=MapperBase)


class ServiceBaseImpl(Generic[M, T], ServiceBase[T]):
    def __init__(self, mapper: Type[M]):
        self.mapper = mapper

    async def save(self, *, record: T) -> T:
        return await self.mapper.insert(record=record)

    async def batch_save(self, *, records: List[T]) -> bool:
        await self.mapper.batch_insert(records=records)
        return True

    async def retrieve_by_id(self, *, id: T) -> T:
        return await self.mapper.select_by_id(id=id)

    async def retrieve_by_ids(self, *, ids: List[T]) -> List[T]:
        return await self.mapper.select_by_ids(ids=ids)

    async def retrieve_records(
        self, *, page: int, size: int, **kwargs
    ) -> Tuple[
        List[Any],
        int,
    ]:
        return await self.mapper.select_pagination(page=page, size=size, **kwargs)

    async def retrieve_ordered_records(
        self,
        *,
        page: int,
        size: int,
        order_by: T = None,
        sort_order: T = None,
        **kwargs,
    ) -> Tuple[
        List[Any],
        int,
    ]:
        return await self.mapper.select_ordered_pagination(
            page=page, size=size, order_by=order_by, sort_order=sort_order, **kwargs
        )

    async def modify_by_id(self, *, update_user_cmd: T) -> bool:
        affect_row: int = await self.mapper.update_by_id(record=update_user_cmd)
        if affect_row != 1:
            raise SystemException(
                SystemResponseCode.PARAMETER_ERROR.code,
                SystemResponseCode.PARAMETER_ERROR.msg,
            )
        return True

    async def batch_modify_by_ids(self, *, ids: List[Any], record: dict, db_session: Any = None) -> bool:
        affect_row: int = await self.mapper.batch_update_by_ids(ids=ids, record=record)
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

    async def batch_remove_by_ids(self, *, ids: List[Any]) -> bool:
        affect_row: int = await self.mapper.batch_delete_by_ids(ids=ids)
        if len(ids) != affect_row:
            raise SystemException(
                SystemResponseCode.DELETE_PARAMETER_ERROR.code,
                SystemResponseCode.DELETE_PARAMETER_ERROR.msg,
            )
        return True
