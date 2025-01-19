from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import String, Float, JSON
from typing import Any, Dict, Optional
from decimal import Decimal

from faslava.config.configuration import settings
from faslava.models import BaseModel


class Product(BaseModel):
    """Primary Product table."""

    __tablename__ = "product"
    __table_args__ = {"schema": settings.ALEMBIC_CUSTOM_SCHEMA}
    __display_name__ = "Product"

    name: Mapped[str] = mapped_column(String(256))
    price: Mapped[Decimal] = mapped_column(Float(precision=2))
    description: Mapped[Optional[str]] = mapped_column(default=None)
    technical_properties: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)

    def __str__(self) -> str:
        return self.name


# class Category(BaseModel, table=True):
#     pass


# class Tag(BaseModel, table=True):
#     pass


# class Order(BaseModel, table=True):
#     """Primary Order table."""
#
#     __tablename__ = "order"
#     __table_args__ = {"schema": settings.ALEMBIC_CUSTOM_SCHEMA}
