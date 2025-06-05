# Copyright (c) 2025 Fast web and/or its affiliates. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""BaseMapper defines the database operations to be implemented"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, Tuple, TypeVar

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

ModelType = TypeVar("ModelType", bound=SQLModel)
IDType = TypeVar("IDType", int, str)


class BaseMapper(ABC, Generic[ModelType]):
    @abstractmethod
    async def insert(self, *, data: ModelType, db_session: Optional[AsyncSession] = None) -> ModelType:
        """Insert a single data into the database.

        Args:
            data: The data to insert
            db_session: Optional async database session. If None, will use default session.

        Returns:
            The inserted data with id
        """
        ...

    @abstractmethod
    async def batch_insert(self, *, data_list: List[ModelType], db_session: Optional[AsyncSession] = None) -> IDType:
        """Insert multiple data_list into the database in a single operation.

        Args:
            data_list: List of data_list to insert
            db_session: Optional async database session

        Returns:
            Number of data_list successfully inserted
        """
        ...

    @abstractmethod
    async def select_by_id(self, *, id: IDType, db_session: Optional[AsyncSession] = None) -> Optional[ModelType]:
        """Retrieve a single data by its ID.

        Args:
            id: The ID of the data to retrieve
            db_session: Optional async database session

        Returns:
            The retrieved data or None if not found
        """
        ...

    @abstractmethod
    async def select_by_ids(self, *, ids: List[IDType], db_session: Optional[AsyncSession] = None) -> List[ModelType]:
        """Retrieve multiple data_list by their IDs.

        Args:
            ids: List of IDs to retrieve
            db_session: Optional async database session

        Returns:
            List of retrieved data_list
        """
        ...

    @abstractmethod
    async def select_by_page(
        self, *, current: IDType, page_size: IDType, db_session: Optional[AsyncSession] = None, **kwargs
    ) -> Tuple[List[ModelType], IDType]:
        """Retrieve data_list with pagination.

        Args:
            current: Current page number (1-based)
            page_size: Number of data_list per page
            db_session: Optional async database session
            **kwargs: Additional filter criteria

        Returns:
            Tuple of (list of data_list for current page, total data count)
        """
        ...

    @abstractmethod
    async def select_by_ordered_page(
        self,
        *,
        current: IDType,
        page_size: IDType,
        order_by: str,
        sort_order: str,
        db_session: Optional[AsyncSession] = None,
        **kwargs,
    ) -> Tuple[List[ModelType], IDType]:
        """Retrieve data_list with pagination and sorting.

        Args:
            current: Current page number (1-based)
            page_size: Number of data_list per page
            order_by: Field to order by
            sort_order: Sort direction ('asc' or 'desc')
            db_session: Optional async database session
            **kwargs: Additional filter criteria

        Returns:
            Tuple of (list of data_list for current page, total data count)
        """
        ...

    @abstractmethod
    async def update_by_id(self, *, data: ModelType, db_session: Optional[AsyncSession] = None) -> IDType:
        """Update a data by its ID.

        Args:
            data: The data data to update (must contain ID)
            db_session: Optional async database session

        Returns:
            Number of data_list updated (0 or 1)
        """
        ...

    @abstractmethod
    async def batch_update_by_ids(
        self, *, ids: List[IDType], data: Dict[str, Any], db_session: Optional[AsyncSession] = None
    ) -> IDType:
        """Update multiple data_list by their IDs with the same values.

        Args:
            ids: List of IDs to update
            data: Dictionary of field-value pairs to update
            db_session: Optional async database session

        Returns:
            Number of data_list updated
        """
        ...

    @abstractmethod
    async def delete_by_id(self, *, id: IDType, db_session: Optional[AsyncSession] = None) -> IDType:
        """Delete a data by its ID.

        Args:
            id: ID of the data to delete
            db_session: Optional async database session

        Returns:
            Number of data_list deleted (0 or 1)
        """
        ...

    @abstractmethod
    async def batch_delete_by_ids(self, *, ids: List[IDType], db_session: Optional[AsyncSession] = None) -> IDType:
        """Delete multiple data_list by their IDs.

        Args:
            ids: List of IDs to delete
            db_session: Optional async database session

        Returns:
            Number of data_list deleted
        """
