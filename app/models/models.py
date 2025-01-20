from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String, Float, JSON
from typing import Any, Dict, List, Optional
from decimal import Decimal

from faslava.config.configuration import settings
from faslava.models import BaseModel

# ProductCategoryAssociation = Table(
#     "product_category_association",
#     BaseModel.metadata,
#     Column("product_id", ForeignKey("product.id")),
#     Column("category_id", ForeignKey("category.id")),
# )


class Product(BaseModel):
    """Primary Product table."""

    __tablename__ = "product"
    __table_args__ = {"schema": settings.ALEMBIC_CUSTOM_SCHEMA}
    __display_name__ = "Product"

    name: Mapped[str] = mapped_column(String(256))
    price: Mapped[Decimal] = mapped_column(Float(precision=2))
    description: Mapped[Optional[str]] = mapped_column(default=None)
    technical_properties: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    # categories: Mapped[List["Category"]] = relationship(
    #     secondary=ProductCategoryAssociation
    # )

    def __str__(self) -> str:
        return self.name


# class Category(BaseModel):
#     __tablename__ = "category"
#     __table_args__ = {"schema": settings.ALEMBIC_CUSTOM_SCHEMA}
#     __display_name__ = "Category"
#
#     name: Mapped[str] = mapped_column(String(256))
#     products: Mapped[List[Product]] = relationship(secondary=ProductCategoryAssociation)


# class Tag(BaseModel):
#     pass


# class Order(BaseModel):
#     """Primary Order table."""
#
#     __tablename__ = "order"
#     __table_args__ = {"schema": settings.ALEMBIC_CUSTOM_SCHEMA}
