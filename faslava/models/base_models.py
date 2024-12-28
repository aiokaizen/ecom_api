from typing import Any, List, Sequence
from sqlmodel import SQLModel
from collections.abc import Iterable

from faslava.serializers.serializers import BaseSerializer


class BaseModel(SQLModel):
    """BaseModel for all the database classes."""

    def serialize(self, data: Any, serializer: BaseSerializer) -> BaseSerializer:
        if not isinstance(data, Iterable):
            return serializer(**data.model_dump())

        for obj in data:
            return serializer(**obj.model_dump())
