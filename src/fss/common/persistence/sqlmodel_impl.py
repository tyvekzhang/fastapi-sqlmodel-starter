"""Sqlmodel impl that do database operations"""

from typing import Generic, TypeVar, List, Any, Type, Union

from fastapi_pagination.ext.sqlmodel import paginate
from pydantic import BaseModel
from sqlmodel import SQLModel, select, func, insert, update, delete
from sqlmodel.ext.asyncio.session import AsyncSession

from fss.common.enum.enum import SortEnum
from fss.common.persistence.base_mapper import BaseMapper
from fss.middleware.db_session_middleware import db

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
SchemaType = TypeVar("SchemaType", bound=BaseModel)
T = TypeVar("T", bound=SQLModel)


class SqlModelMapper(Generic[ModelType], BaseMapper):
    def __init__(self, model: Type[ModelType]):
        self.model = model
        self.db = db

    def get_db_session(self) -> Type[Any]:
        return self.db

    async def insert(
        self,
        *,
        data: Union[ModelType, SchemaType],
        db_session: Union[AsyncSession, None] = None,
    ) -> int:
        db_session = db_session or self.db.session
        orm_data = self.model.model_validate(data)
        db_session.add(orm_data)
        return orm_data

    async def insert_batch(
        self, *, data_list: List[Any], db_session: Any = None
    ) -> int:
        db_session = db_session or self.db.session
        orm_datas = []
        for data in data_list:
            orm_datas.append(self.model.model_validate(data))
        statement = insert(self.model).values([data.model_dump() for data in orm_datas])
        await db_session.execute(statement)
        return len(data_list)

    async def select_by_id(self, *, id: Any, db_session: Any = None) -> Any:
        db_session = db_session or self.db.session
        statement = select(self.model).where(self.model.id == id)
        response = await db_session.execute(statement)
        return response.scalar_one_or_none()

    async def select_by_ids(
        self, *, ids: List[Any], batch_size: int = 1000, db_session: Any = None
    ) -> List[Any]:
        db_session = db_session or self.db.session
        result_set = []
        for i in range(0, len(ids), batch_size):
            batch_ids = ids[i : i + batch_size]
            statement = select(self.model).where(self.model.id.in_(batch_ids))
            results = await db_session.exec(statement).all()
            result_set.extend(results)
        return result_set

    async def select_count(self, *, db_session: Any = None) -> int:
        db_session = db_session or self.db.session
        response = await db_session.execute(
            select(func.count()).select_from(select(self.model).subquery())
        )
        return response.scalar_one()

    async def select_list(
        self, *, page: int = 1, size: int = 100, query: Any, db_session: Any = None
    ) -> List[Any]:
        db_session = db_session or self.db.session
        if query is None:
            query = (
                select(self.model)
                .offset((page - 1) * size)
                .limit(size)
                .order_by(self.model.id)
            )
        response = await db_session.execute(query)
        return response.scalars().all()

    async def select_list_ordered(
        self,
        *,
        page: int = 1,
        size: int = 100,
        query: Any,
        order_by: Any,
        sort_order: Any,
        db_session: Any = None,
    ) -> List[Any]:
        db_session = db_session or self.db.session
        columns = self.model.__table__.columns
        if order_by is None or order_by not in columns:
            order_by = "id"
        if sort_order == SortEnum.ascending:
            query = (
                select(self.model)
                .offset((page - 1) * size)
                .limit(size)
                .order_by(columns[order_by].asc())
            )
        else:
            query = (
                select(self.model)
                .offset((page - 1) * size)
                .limit(size)
                .order_by(columns[order_by].desc())
            )
        response = await db_session.execute(query)
        return response.scalars().all()

    async def select_list_page(
        self, *, params: Any, query: Any, db_session: Any = None
    ) -> List[Any]:
        db_session = db_session or self.db.session
        if query is None:
            query = select(self.model)
        response = await paginate(db_session, query, params)
        return response

    async def select_list_page_ordered(
        self,
        *,
        params: Any,
        query: Any = None,
        order_by: Any = None,
        sort_order: Any = None,
        db_session: Any = None,
    ) -> List[Any]:
        db_session = db_session or self.db.session
        columns = self.model.__table__.columns
        if order_by is None or order_by not in columns:
            order_by = "id"
        if query is None:
            if sort_order == SortEnum.ascending:
                query = select(self.model).order_by(columns[order_by].asc())
            else:
                query = select(self.model).order_by(columns[order_by].desc())
        return await paginate(db_session, query, params)

    async def update_by_id(self, *, data: Any, db_session: Any = None) -> int:
        db_session = db_session or self.db.session
        query = select(self.model).where(self.model.id == data.id)
        result = await db_session.execute(query)
        if result is None:
            return 0
        db_data = result.scalar_one()
        if isinstance(data, dict):
            update_data = data
        else:
            update_data = data.model_dump(exclude_unset=True)
        for field in update_data:
            setattr(db_data, field, update_data[field])

        db_session.add(db_data)
        return db_data

    async def update_batch_by_ids(
        self, *, data_list: List[Any], db_session: Any = None
    ) -> int:
        db_session = db_session or self.db.session
        for data in data_list:
            if hasattr(data, "id"):
                statement = (
                    update(self.model)
                    .where(self.model.id == data.id)
                    .values(**data.dict(exclude_unset=True))
                )
                await db_session.execute(statement)
        return len(data_list)

    async def delete_by_id(self, *, id: Any, db_session: Any = None) -> int:
        db_session = db_session or self.db.session
        statement = select(self.model).where(self.model.id == id)
        response = await db_session.execute(statement)
        data = response.scalar_one()
        return await db_session.delete(data)

    async def delete_batch_by_ids(
        self, *, ids: List[Any], db_session: Any = None
    ) -> int:
        db_session = db_session or self.db.session
        statement = delete(self.model).where(self.model.id.in_(ids))
        result = await db_session.execute(statement)
        return result.rowcount
