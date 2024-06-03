"""Sqlmodel impl that do database operations"""

from typing import Generic, TypeVar, List, Any, Type, Union, Tuple

from pydantic import BaseModel
from sqlalchemy import func
from sqlmodel import SQLModel, select, insert, update, delete
from sqlmodel.ext.asyncio.session import AsyncSession

from fss.common.enum.enum import SortEnum
from fss.common.persistence.base_mapper import BaseMapper
from fss.middleware.db_session_middleware import db

ModelType = TypeVar("ModelType", bound=SQLModel)
SchemaType = TypeVar("SchemaType", bound=BaseModel)
T = TypeVar("T", bound=SQLModel)


class SqlModelMapper(Generic[ModelType], BaseMapper):
    def __init__(self, model: Type[ModelType]):
        self.model = model
        self.db = db

    async def insert_record(
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
        orm_record = self.model.model_validate(record)
        db_session.add(orm_record)
        return orm_record

    async def batch_insert_records(
        self, *, records: List[Any], db_session: Any = None
    ) -> int:
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
        statement = insert(self.model).values(
            [record.model_dump() for record in orm_records]
        )
        exec_response = await db_session.execute(statement)
        return exec_response.rowcount

    async def select_record_by_id(
        self, *, id: Any, db_session: Any = None
    ) -> Union[ModelType, SchemaType]:
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
        exec_response = await db_session.execute(statement)
        return exec_response.scalar_one_or_none()

    async def select_records(
        self, *, page: int = 1, size: int = 100, db_session: Any = None, **kwargs
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
        if "filter_by" in kwargs:
            query = query.filter_by(**kwargs["filter_by"])
        elif "filter" in kwargs:
            query = query.filter(kwargs["filter"])
        if "like" in kwargs:
            for column, value in kwargs["like"].items():
                query = query.filter(getattr(self.model, column).like(value))

        count_query = select(func.count()).select_from(query.subquery())
        total_count_result = await db_session.execute(count_query)
        total_count = total_count_result.scalar()

        paginated_query = query.offset((page - 1) * size).limit(size)
        exec_response = await db_session.execute(paginated_query)
        records = exec_response.scalars().all()

        return records, total_count

    async def select_ordered_records(
        self,
        *,
        page: int = 1,
        size: int = 100,
        order_by: Any = None,
        sort_order: Any = None,
        db_session: Any = None,
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
        if "filter_by" in kwargs:
            query = query.filter_by(**kwargs["filter_by"])
        elif "filter" in kwargs:
            query = query.filter(kwargs["filter"])
        if "like" in kwargs:
            for column, value in kwargs["like"].items():
                query = query.filter(getattr(self.model, column).like(value))
        columns = self.model.__table__.columns
        if order_by is None or order_by not in columns:
            order_by = "id"
        if sort_order is None or sort_order == SortEnum.ascending:
            query = (
                query.offset((page - 1) * size)
                .limit(size)
                .order_by(columns[order_by].asc())
            )
        else:
            query = (
                query.offset((page - 1) * size)
                .limit(size)
                .order_by(columns[order_by].des())
            )
        count_query = select(func.count()).select_from(query.subquery())
        total_count_result = await db_session.execute(count_query)
        total_count = total_count_result.scalar()

        exec_response = await db_session.execute(query)
        records = exec_response.scalars().all()
        return records, total_count

    async def update_record_by_id(self, *, record: Any, db_session: Any = None) -> int:
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
        exec_response = await db_session.execute(update_query)
        return exec_response.rowcount

    async def batch_update_records_by_ids(
        self, *, ids: List[Any], record: dict, db_session: Any = None
    ) -> int:
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
        exec_response = await db_session.execute(statement)
        return exec_response.rowcount

    async def delete_record_by_id(self, *, id: Any, db_session: Any = None) -> int:
        """
        Delete a single record by its ID.

        Parameters:
            id : The ID of the record to delete
            db_session : The database session to use
        """
        db_session = db_session or self.db.session
        statement = delete(self.model).where(self.model.id == id)
        exec_response = await db_session.execute(statement)
        return exec_response.rowcount

    async def batch_delete_records_by_ids(
        self, *, ids: List[Any], db_session: Any = None
    ) -> int:
        """
        Delete multiple records by their IDs.

        Parameters:
            ids : The IDs of the records to update
            db_session : The database session to use
        """
        db_session = db_session or self.db.session
        statement = delete(self.model).where(self.model.id.in_(ids))
        exec_response = await db_session.execute(statement)
        return exec_response.rowcount
