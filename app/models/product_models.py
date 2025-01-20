from sqlalchemy import Column, ForeignKey, Table, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import REAL, DateTime, String, JSON
from typing import Any, Dict, List, Optional
from decimal import Decimal

from faslava.models import BaseModel


ProductCategoryAssociation = Table(
    "product_category_association",
    BaseModel.metadata,
    Column("product_id", ForeignKey("product.id")),
    Column("category_id", ForeignKey("category.id")),
    Column("created_at", DateTime(), server_default=text("CURRENT_TIMESTAMP")),
)


class Product(BaseModel):
    """Primary Product table."""

    __tablename__ = "product"
    __display_name__ = "Product"

    name: Mapped[str] = mapped_column(String(256))
    price: Mapped[Decimal] = mapped_column(REAL(precision=2))
    description: Mapped[Optional[str]] = mapped_column(default=None)
    technical_properties: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    tags: Mapped[Optional[List[str]]] = mapped_column(JSON)
    categories: Mapped[List["Category"]] = relationship(
        secondary=ProductCategoryAssociation
    )

    def __str__(self) -> str:
        return self.name


class Category(BaseModel):
    __tablename__ = "category"
    __display_name__ = "Category"

    name: Mapped[str] = mapped_column(String(256))
    products: Mapped[List[Product]] = relationship(secondary=ProductCategoryAssociation)

    def __str__(self) -> str:
        return self.name


class Tag(BaseModel):
    __tablename__ = "tag"
    __display_name__ = "Tag"

    name: Mapped[str] = mapped_column(String(256))


# class Order(BaseModel):
#     """Primary Order table."""
#
#     __tablename__ = "order"
