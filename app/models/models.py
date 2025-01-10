from pydantic import field_serializer
from sqlalchemy import Column
from sqlalchemy.types import String
from sqlmodel import Field, Relationship
from typing import List, Optional
from decimal import Decimal

from enums.enums import TechnicalPropertyEnum
from faslava.config.configuration import settings
from faslava.models import BaseModel
from faslava.core.utils import gettext_lazy as _


class TechnicalProperty(BaseModel, table=True):
    """Primary Product table."""

    __tablename__ = "technical_properties"
    __table_args__ = {"schema": settings.ALEMBIC_CUSTOM_SCHEMA}

    id: Optional[int] = Field(primary_key=True, description=_("ID"))
    product_id: int = Field(
        description="Product ID",
        foreign_key=f"{settings.ALEMBIC_CUSTOM_SCHEMA}.product.id",
    )
    name: TechnicalPropertyEnum = Field(
        description=_("Name"), sa_column=Column(String(length=25))
    )
    value: str = Field(description=_("Value"))
    product: Optional["Product"] = Relationship(back_populates="technical_properties")


class Product(BaseModel, table=True):
    """Primary Product table."""

    __tablename__ = "product"
    __table_args__ = {"schema": settings.ALEMBIC_CUSTOM_SCHEMA}

    id: Optional[int] = Field(primary_key=True, description=_("ID"))
    name: str = Field(max_length=256, description=_("Name"))
    price: Decimal = Field(decimal_places=2, max_digits=11, description=_("Price"))
    description: Optional[str] = Field(default="", description=_("Description"))
    technical_properties: List[TechnicalProperty] = Relationship(
        back_populates="product"
    )

    @field_serializer("technical_properties", check_fields=False)
    def serialize_technical_properties(self, value: List[TechnicalProperty]):
        print("Serializing technical_properties...\n\n")
        return [v.model_dump() for v in value]


# class Order(BaseModel, table=True):
#     """Primary Order table."""
#
#     __tablename__ = "order"
#     __table_args__ = {"schema": settings.ALEMBIC_CUSTOM_SCHEMA}
