"""Sqlmodel impl that handle database operation"""

from typing import Generic, TypeVar, List, Any, Type, Union, Tuple, Optional

from pydantic import BaseModel
from sqlmodel import SQLModel, select, insert, update, delete, func
from sqlmodel.ext.asyncio.session import AsyncSession

from src.main.app.common.enums.enum import SortEnum, FilterOperators
from src.main.app.common.mapper.mapper_base import MapperBase
from src.main.app.common.session.db_session_middleware import db

ModelType = TypeVar("ModelType", bound=SQLModel)
SchemaType = TypeVar("SchemaType", bound=BaseModel)
T = TypeVar("T", bound=SQLModel)


class SqlModelMapper(Generic[ModelType], MapperBase):
    def __init__(self, model: Type[ModelType]):
        self.model = model
        self.db = db

    async def insert(
        self,
        *,
        record: Union[ModelType, SchemaType],
        db_session: Union[AsyncSession, None] = None,
    ) -> Union[ModelType, SchemaType]:
        """
        Inserts a single record into the database.

        Args:
            record: The record to be inserted.
            db_session: The database session to use. If None, uses the default session.

        Returns:
            The record with ID.
        """
        db_session = db_session or self.db.session
        record = self.model.model_validate(record)
        db_session.add(record)
        return record

    async def batch_insert(self, *, records: List[Any], db_session: AsyncSession = None) -> int:
        """
        Inserts multiple records into the database in a single batch.

        Args:
            records: A list of record to be inserted, each item either a Model instance or a Schema dict.
            db_session: The database session to use. If None, uses the default session.

        Returns:
            The number of records inserted.
        """
        db_session = db_session or self.db.session
        orm_records = [self.model.model_validate(record) for record in records]
        statement = insert(self.model).values([record.model_dump() for record in orm_records])
        exec_response = await db_session.exec(statement)
        return exec_response.rowcount

    async def select_by_id(self, *, id: Any, db_session: AsyncSession = None) -> Union[ModelType, SchemaType]:
        """
        Select a single record by its ID.

        Args:
            id: The ID of the record to retrieve.
            db_session: The database session to use. If None, uses the default session.

        Returns:
            The retrieved record, or None if not found.
        """
        db_session = db_session or self.db.session
        statement = select(self.model).where(self.model.id == id)
        exec_response = await db_session.exec(statement)
        return exec_response.one_or_none()

    async def select_by_ids(self, *, ids: List[Any], db_session: AsyncSession = None) -> List[Any]:
        """
        Select records by a list of ID.

        Args:
            ids: The IDs of the records to retrieve.
            db_session: The database session to use. If None, uses the default session.

        Returns:
            The retrieved records, or None if not found.
        """
        db_session = db_session or self.db.session
        statement = select(self.model).where(self.model.id.in_(ids))
        exec_response = await db_session.exec(statement)
        return exec_response.all()

    async def select_by_page(
        self,
        *,
        current: int = 1,
        pageSize: int = 100,
        count: bool = True,
        db_session: AsyncSession = None,
        **kwargs,
    ) -> Tuple[List[Any], int]:
        """
        Retrieve a list of records, with optional filtering, pagination, and ordering.

        Parameters:
            current : The current page number to retrieve (1-indexed)
            pageSize : The number of records per page
            count : Whether to record the total row
            db_session : The database session to use
            **kwargs: Additional filter criteria, including:
                - EQ: Equal to (e.g., {"column_name": value})
                - NE: Not equal to (e.g., {"column_name": value})
                - GT: Greater than (e.g., {"column_name": value})
                - GE: Greater than or equal to (e.g., {"column_name": value})
                - LT: Less than (e.g., {"column_name": value})
                - LE: Less than or equal to (e.g., {"column_name": value})
                - BETWEEN: Between two values (e.g., {"column_name": (start, end)})
                - LIKE: Fuzzy search (e.g., {"column_name": "%value%"})
        """
        db_session = db_session or self.db.session
        query = select(self.model)

        # 处理过滤条件
        if FilterOperators.EQ in kwargs:
            for column, value in kwargs[FilterOperators.EQ].items():
                query = query.filter(getattr(self.model, column) == value)
        if FilterOperators.NE in kwargs:
            for column, value in kwargs[FilterOperators.NE].items():
                query = query.filter(getattr(self.model, column) != value)
        if FilterOperators.GT in kwargs:
            for column, value in kwargs[FilterOperators.GT].items():
                query = query.filter(getattr(self.model, column) > value)
        if FilterOperators.GE in kwargs:
            for column, value in kwargs[FilterOperators.GE].items():
                query = query.filter(getattr(self.model, column) >= value)
        if FilterOperators.LT in kwargs:
            for column, value in kwargs[FilterOperators.LT].items():
                query = query.filter(getattr(self.model, column) < value)
        if FilterOperators.LE in kwargs:
            for column, value in kwargs[FilterOperators.LE].items():
                query = query.filter(getattr(self.model, column) <= value)
        if FilterOperators.BETWEEN in kwargs:
            for column, (start, end) in kwargs[FilterOperators.BETWEEN].items():
                query = query.filter(getattr(self.model, column).between(start, end))
        if FilterOperators.LIKE in kwargs:
            for column, value in kwargs[FilterOperators.LIKE].items():
                query = query.filter(getattr(self.model, column).like(value))

        # 计算总数
        if count:
            count_query = select(func.count()).select_from(query.subquery())
            total_count_result = await db_session.exec(count_query)
            total_count: int = total_count_result.all()[0]
        else:
            total_count = 0

        # 分页
        query = query.offset((current - 1) * pageSize).limit(pageSize)

        # 执行查询
        exec_response = await db_session.exec(query)
        records: List[Any] = exec_response.all()

        return records, total_count

    async def select_by_ordered_page(
        self,
        *,
        current: int = 1,
        pageSize: int = 100,
        count: bool = True,
        order_by: Optional[str] = None,
        sort_order: Optional[str] = SortEnum.ascending,
        db_session: AsyncSession = None,
        **kwargs,
    ) -> Tuple[List[Any], int]:
        """
        Retrieve a list of records, with optional filtering, pagination, and ordering.

        Parameters:
            current : The current page number to retrieve (1-indexed)
            pageSize : The number of records per page
            count : Whether to record the total row
            order_by : The column to order by
            sort_order : The sort order (ascending or descending)
            db_session : The database session to use
            **kwargs: Additional filter criteria, including:
                - EQ: Equal to (e.g., {"column_name": value})
                - NE: Not equal to (e.g., {"column_name": value})
                - GT: Greater than (e.g., {"column_name": value})
                - GE: Greater than or equal to (e.g., {"column_name": value})
                - LT: Less than (e.g., {"column_name": value})
                - LE: Less than or equal to (e.g., {"column_name": value})
                - BETWEEN: Between two values (e.g., {"column_name": (start, end)})
                - LIKE: Fuzzy search (e.g., {"column_name": "%value%"})
        """
        db_session = db_session or self.db.session
        query = select(self.model)

        # 处理过滤条件
        if FilterOperators.EQ in kwargs:
            for column, value in kwargs[FilterOperators.EQ].items():
                query = query.filter(getattr(self.model, column) == value)
        if FilterOperators.NE in kwargs:
            for column, value in kwargs[FilterOperators.NE].items():
                query = query.filter(getattr(self.model, column) != value)
        if FilterOperators.GT in kwargs:
            for column, value in kwargs[FilterOperators.GT].items():
                query = query.filter(getattr(self.model, column) > value)
        if FilterOperators.GE in kwargs:
            for column, value in kwargs[FilterOperators.GE].items():
                query = query.filter(getattr(self.model, column) >= value)
        if FilterOperators.LT in kwargs:
            for column, value in kwargs[FilterOperators.LT].items():
                query = query.filter(getattr(self.model, column) < value)
        if FilterOperators.LE in kwargs:
            for column, value in kwargs[FilterOperators.LE].items():
                query = query.filter(getattr(self.model, column) <= value)
        if FilterOperators.BETWEEN in kwargs:
            for column, (start, end) in kwargs[FilterOperators.BETWEEN].items():
                query = query.filter(getattr(self.model, column).between(start, end))
        if FilterOperators.LIKE in kwargs:
            for column, value in kwargs[FilterOperators.LIKE].items():
                query = query.filter(getattr(self.model, column).like(value))

        # 计算总数
        if count:
            count_query = select(func.count()).select_from(query.subquery())
            total_count_result = await db_session.exec(count_query)
            total_count: int = total_count_result.all()[0]
        else:
            total_count = 0

        # 处理排序
        columns = self.model.__table__.columns
        if order_by is None or order_by not in columns:
            order_by = "id"
        if sort_order == SortEnum.ascending:
            query = query.order_by(getattr(self.model, order_by).asc())
        else:
            query = query.order_by(getattr(self.model, order_by).desc())

        # 分页
        query = query.offset((current - 1) * pageSize).limit(pageSize)

        # 执行查询
        exec_response = await db_session.exec(query)
        records: List[Any] = exec_response.all()

        return records, total_count

    async def update_by_id(self, *, record: Any, db_session: AsyncSession = None) -> int:
        """
        Update a single record by its ID.

        Parameters:
            record : The data to update
            db_session : The database session to use
        """
        db_session = db_session or self.db.session
        update_query = update(self.model).where(self.model.id == record.id)
        update_values = record.model_dump(exclude_unset=True)
        update_query = update_query.values(**update_values)
        exec_response = await db_session.exec(update_query)
        return exec_response.rowcount

    async def batch_update_by_ids(self, *, ids: List[Any], record: dict, db_session: AsyncSession = None) -> int:
        """
        Update multiple records by their IDs.

        Parameters:
            ids : The IDs of the records to update
            record : The data to update
            db_session : The database session to use
        """
        db_session = db_session or self.db.session
        statement = update(self.model).where(self.model.id.in_(ids))
        for key, value in record.items():
            statement = statement.values({key: value})
        exec_response = await db_session.exec(statement)
        return exec_response.rowcount

    async def delete_by_id(self, *, id: Any, db_session: AsyncSession = None) -> int:
        """
        Delete a single record by its ID.

        Parameters:
            id : The ID of the record to delete
            db_session : The database session to use
        """
        db_session = db_session or self.db.session
        statement = delete(self.model).where(self.model.id == id)
        exec_response = await db_session.exec(statement)
        return exec_response.rowcount

    async def batch_delete_by_ids(self, *, ids: List[Any], db_session: AsyncSession = None) -> int:
        """
        Delete multiple records by their IDs.

        Parameters:
            ids : The IDs of the records to update
            db_session : The database session to use
        """
        db_session = db_session or self.db.session
        statement = delete(self.model).where(self.model.id.in_(ids))
        exec_response = await db_session.exec(statement)
        return exec_response.rowcount
