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
"""Abstract Service used in the project"""

from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic, Tuple, Union, Dict

from sqlmodel import SQLModel

T = TypeVar("T", bound=SQLModel)


class BaseService(Generic[T], ABC):
    """Abstract base class defining the interface for service operations."""

    @abstractmethod
    async def save(self, *, data: T) -> T:
        """Save a single model."""
        ...

    @abstractmethod
    async def batch_save(self, *, data: List[T]) -> int:
        """Save multiple entities, returns count of saved items."""
        ...

    @abstractmethod
    async def retrieve_by_id(self, *, id: Union[int, str]) -> T:
        """Retrieve an model by its ID."""
        ...

    @abstractmethod
    async def retrieve_by_ids(
        self, *, ids: Union[List[int], List[str]]
    ) -> List[T]:
        """Retrieve multiple entities by their IDs."""
        ...

    @abstractmethod
    async def retrieve_data(
        self, *, page: int, size: int, **kwargs
    ) -> Tuple[List[T], int]:
        """Retrieve paginated data with optional filters."""
        ...

    @abstractmethod
    async def retrieve_ordered_data(
        self, *, page: int, size: int, order_by: str, sort_order: str, **kwargs
    ) -> Tuple[List[T], int]:
        """Retrieve paginated data with sorting."""
        ...

    @abstractmethod
    async def modify_by_id(self, *, data: T) -> None:
        """Update an existing model by ID."""
        ...

    @abstractmethod
    async def batch_modify_by_ids(
        self, *, ids: Union[List[int], List[str]], data: Dict
    ) -> None:
        """Update multiple entities by their IDs."""
        ...

    @abstractmethod
    async def remove_by_id(self, *, id: Union[int, str]) -> None:
        """Delete an model by its ID."""
        ...

    @abstractmethod
    async def batch_remove_by_ids(
        self, *, ids: Union[List[int], List[str]]
    ) -> None:
        """Delete multiple entities by their IDs."""
        ...
