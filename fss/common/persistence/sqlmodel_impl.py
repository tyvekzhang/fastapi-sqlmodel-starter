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

    async def insert(
        self,
        *,
        data: Union[ModelType, SchemaType],
        db_session: Union[AsyncSession, None] = None,
    ) -> Any:
        """
        Inserts a single row into the database.

        Args:
            data: The data to be inserted, either a Model instance or a Schema dict.
            db_session: The database session to use. If None, uses the default session.

        Returns:
            The inserted row with ID.
        """
        db_session = db_session or self.db.session
        orm_data = self.model.model_validate(data)
        db_session.add(orm_data)
        return orm_data

    async def insert_batch(
        self, *, data_list: List[Any], db_session: Any = None
    ) -> int:
        """
        Inserts multiple rows into the database in a single batch.

        Args:
            data_list: A list of data to be inserted, each item either a Model instance or a Schema dict.
            db_session: The database session to use. If None, uses the default session.

        Returns:
            The number of rows inserted.
        """
        db_session = db_session or self.db.session
        orm_datas = [self.model.model_validate(data) for data in data_list]
        statement = insert(self.model).values([data.model_dump() for data in orm_datas])
        result = await db_session.execute(statement)
        return result.rowcount

    async def select_by_id(self, *, id: Any, db_session: Any = None) -> Any:
        """
        Retrieves a single row by its ID.

        Args:
            id: The ID of the row to retrieve.
            db_session: The database session to use. If None, uses the default session.

        Returns:
            The retrieved row, or None if not found.
        """
        db_session = db_session or self.db.session
        statement = select(self.model).where(self.model.id == id)
        response = await db_session.execute(statement)
        return response.scalar_one_or_none()

    async def select_count(self, *, db_session: Any = None) -> int:
        """
        Retrieves the total count of rows in the table.

        Args:
            db_session: The database session to use. If None, uses the default session.

        Returns:
            The total count of rows.
        """
        db_session = db_session or self.db.session
        response = await db_session.execute(
            select(func.count()).select_from(select(self.model).subquery())
        )
        return response.scalar_one()

    async def select_list(
        self, *, page: int = 1, size: int = 100, db_session: Any = None, **kwargs
    ) -> List[Any]:
        """
        Retrieves a list of rows, with optional filtering and pagination.

        Args:
            page: The page number to retrieve (1-indexed).
            size: The number of rows per page.
            db_session: The database session to use. If None, uses the default session.
            **kwargs: Additional filter criteria, such as `filter_by` or `like`.

        Returns:
            A list of retrieved rows.
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
        query = query.offset((page - 1) * size).limit(size).order_by(self.model.id)
        response = await db_session.execute(query)
        return response.scalars().all()

    async def select_list_ordered(
        self,
        *,
        page: int = 1,
        size: int = 100,
        order_by: Any = None,
        sort_order: Any = None,
        db_session: Any = None,
        **kwargs,
    ) -> List[Any]:
        """
        Retrieve a list of rows, with optional filtering, pagination, and ordering.

        Parameters:
            page : The page number to retrieve (1-indexed)
            size : The number of rows per page
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
        response = await db_session.execute(query)
        return response.scalars().all()

    async def select_page(self, *, params: Any, db_session: Any = None) -> List[Any]:
        """
        Retrieve a page of rows, with optional filtering and pagination.

        Parameters:
            params : The pagination parameters
            db_session : The database session to use
        """
        db_session = db_session or self.db.session
        query = select(self.model)
        return await paginate(db_session, query, params)

    async def select_page_ordered(
        self,
        *,
        params: Any,
        order_by: Any = None,
        sort_order: Any = None,
        db_session: Any = None,
    ) -> List[Any]:
        """
        Retrieve a page of rows, with optional filtering, pagination, and ordering.

        Parameters:
            params : The pagination parameters
            order_by : The column to order by
            sort_order : The sort order (ascending or descending)
            db_session : The database session to use
        """
        db_session = db_session or self.db.session
        columns = self.model.__table__.columns
        if order_by is None or order_by not in columns:
            order_by = "id"
        if sort_order == SortEnum.ascending:
            query = select(self.model).order_by(columns[order_by].asc())
        else:
            query = select(self.model).order_by(columns[order_by].desc())
        return await paginate(db_session, query, params)

    async def update_by_id(self, *, data: Any, db_session: Any = None) -> int:
        """
        Update a single row by its ID.

        Parameters:
            data : The data to update
            db_session : The database session to use
        """
        db_session = db_session or self.db.session
        query = update(self.model).where(self.model.id == data.id)
        values = data.model_dump(exclude_unset=True)
        query = query.values(**values)
        result = await db_session.execute(query)
        return result.rowcount

    async def update_batch_by_ids(
        self, *, ids: List[Any], data: dict, db_session: Any = None
    ) -> int:
        """
        Update multiple rows by their IDs.

        Parameters:
            ids : The IDs of the rows to update
            data : The data to update
            db_session : The database session to use
        """
        async with db_session or self.db.session as session:
            statement = update(self.model).where(self.model.id.in_(ids))
            for key, value in data.items():
                statement = statement.values({key: value})
            result = await session.execute(statement)
            return result.rowcount

    async def delete_by_id(self, *, id: Any, db_session: Any = None) -> int:
        """
        Delete a single row by its ID.

        Parameters:
            id : The ID of the row to delete
            db_session : The database session to use
        """
        db_session = db_session or self.db.session
        statement = delete(self.model).where(self.model.id == id)
        result = await db_session.execute(statement)
        return result.rowcount

    async def delete_batch_by_ids(
        self, *, ids: List[Any], db_session: Any = None
    ) -> int:
        """
        Delete multiple rows by their IDs.

        Parameters:
            ids : The IDs of the rows to update
            db_session : The database session to use
        """
        db_session = db_session or self.db.session
        statement = delete(self.model).where(self.model.id.in_(ids))
        result = await db_session.execute(statement)
        return result.rowcount
