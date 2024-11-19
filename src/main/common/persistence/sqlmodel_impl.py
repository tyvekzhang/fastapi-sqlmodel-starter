"""Sqlmodel impl that do database operations"""

from typing import Generic, TypeVar, List, Any, Type, Union, Tuple

from pydantic import BaseModel
from sqlmodel import SQLModel, select, insert, update, delete, func
from sqlmodel.ext.asyncio.session import AsyncSession

from src.main.common.enum.enum import SortEnum
from src.main.common.persistence.mapper_base import MapperBase
from src.main.common.middleware.db_session_middleware import db

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

    async def select_pagination(
        self,
        *,
        page: int = 1,
        size: int = 100,
        db_session: AsyncSession = None,
        **kwargs,
    ) -> Tuple[
        List[Any],
        int,
    ]:
        """
        Select a list of records, with optional filtering and pagination.

        Args:
            page: The page number to retrieve (1-indexed).
            size: The number of records per page.
            db_session: The database session to use. If None, uses the default session.
            **kwargs: Additional filter criteria, such as `filter_by` or `like`.

        Returns:
            A list of retrieved records.
        """
        db_session = db_session or self.db.session
        query = select(self.model)
        if "filter_by" in kwargs and kwargs["filter_by"]:
            query = query.filter_by(**kwargs["filter_by"])
        if "like" in kwargs and kwargs["like"]:
            for column, value in kwargs["like"].items():
                query = query.filter(getattr(self.model, column).like(value))
        if "between" in kwargs and kwargs["between"]:
            for column, (start, end) in kwargs["between"].items():
                query = query.filter(getattr(self.model, column).between(start, end))
        if "greater_than" in kwargs and kwargs["greater_than"]:
            for column, value in kwargs["greater_than"].items():
                query = query.filter(getattr(self.model, column) > value)
        if "less_than" in kwargs and kwargs["less_than"]:
            for column, value in kwargs["less_than"].items():
                query = query.filter(getattr(self.model, column) < value)
        count_query = query
        total_count = 0
        if "count" in kwargs and kwargs["count"]:
            count_query = select(func.count()).select_from(count_query.subquery())
            total_count_result = await db_session.exec(count_query)
            total_count: int = total_count_result.all()[0]

        paginated_query = query.offset((page - 1) * size).limit(size)
        exec_response = await db_session.exec(paginated_query)
        records = exec_response.all()

        return records, total_count

    async def select_ordered_pagination(
        self,
        *,
        page: int = 1,
        size: int = 100,
        order_by: Any = None,
        sort_order: Any = None,
        db_session: AsyncSession = None,
        **kwargs,
    ) -> Tuple[
        List[Any],
        int,
    ]:
        """
        Retrieve a list of records, with optional filtering, pagination, and ordering.

        Parameters:
            page : The page number to retrieve (1-indexed)
            size : The number of records per page
            order_by : The column to order by
            sort_order : The sort order (ascending or descending)
            db_session : The database session to use
            **kwargs: Additional filter criteria
        """
        db_session = db_session or self.db.session
        query = select(self.model)
        if "filter_by" in kwargs and kwargs["filter_by"]:
            query = query.filter_by(**kwargs["filter_by"])
        if "like" in kwargs and kwargs["like"]:
            for column, value in kwargs["like"].items():
                query = query.filter(getattr(self.model, column).like(value))
        if "between" in kwargs and kwargs["between"]:
            for column, (start, end) in kwargs["between"].items():
                query = query.filter(getattr(self.model, column).between(start, end))
        if "greater_than" in kwargs and kwargs["greater_than"]:
            for column, value in kwargs["greater_than"].items():
                query = query.filter(getattr(self.model, column) > value)
        if "less_than" in kwargs and kwargs["less_than"]:
            for column, value in kwargs["less_than"].items():
                query = query.filter(getattr(self.model, column) < value)
        count_query = query
        columns = self.model.__table__.columns
        if order_by is None or order_by not in columns:
            order_by = "id"
        if sort_order is None or sort_order == SortEnum.descending:
            query = query.offset((page - 1) * size).limit(size).order_by(columns[order_by].desc())
        else:
            query = query.offset((page - 1) * size).limit(size).order_by(columns[order_by].acs())
        total_count = 0
        if "count" in kwargs and kwargs["count"]:
            count_query = select(func.count()).select_from(count_query.subquery())
            total_count_result = await db_session.exec(count_query)
            total_count: int = total_count_result.all()[0]

        exec_response = await db_session.exec(query)
        records = exec_response.all()
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
