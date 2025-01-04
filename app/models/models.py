from sqlalchemy import Column
from sqlalchemy.types import String
from sqlmodel import Field
from typing import Optional
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
    product_id: int = Field(description="Product ID", foreign_key="almbc.product.id")
    name: TechnicalPropertyEnum = Field(
        description=_("Name"), sa_column=Column(String(length=25))
    )
    value: str = Field(description=_("Value"))


class Product(BaseModel, table=True):
    """Primary Product table."""

    __tablename__ = "product"
    __table_args__ = {"schema": settings.ALEMBIC_CUSTOM_SCHEMA}

    id: Optional[int] = Field(primary_key=True, description=_("ID"))
    name: str = Field(max_length=256, description=_("Name"))
    price: Decimal = Field(decimal_places=2, max_digits=11, description=_("Price"))
    description: Optional[str] = Field(default="", description=_("Description"))
    technical_properties: str = Field(default="", description=_("Technical Properties"))


# class Command(BaseModel, table=True):
#     """Primary Product table."""
#
#     __tablename__ = "command"
#     __table_args__ = {"schema": settings.ALEMBIC_CUSTOM_SCHEMA}
