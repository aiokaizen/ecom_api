from pydantic import field_serializer
from sqlalchemy import Column
from sqlalchemy.types import String
from sqlmodel import JSON, Field
from typing import Optional
from decimal import Decimal

from faslava.config.configuration import settings
from faslava.models import BaseModel
from faslava.core.utils import gettext_lazy as _


class Product(BaseModel, table=True):
    """Primary Product table."""

    __tablename__ = "product"
    __table_args__ = {"schema": settings.ALEMBIC_CUSTOM_SCHEMA}
    __display_name__ = "Product"

    id: Optional[int] = Field(primary_key=True, description=_("ID"))
    name: str = Field(max_length=256, description=_("Name"))
    price: Decimal = Field(decimal_places=2, max_digits=11, description=_("Price"))
    description: Optional[str] = Field(default="", description=_("Description"))
    technical_properties: Optional[dict] = Field(
        default=None, sa_column=Column(JSON, nullable=True)
    )


# class Order(BaseModel, table=True):
#     """Primary Order table."""
#
#     __tablename__ = "order"
#     __table_args__ = {"schema": settings.ALEMBIC_CUSTOM_SCHEMA}
