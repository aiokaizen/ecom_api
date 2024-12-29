from sqlmodel import Field, Session, SQLModel
from typing import Optional
from decimal import Decimal

from enums.enums import TechnicalPropertyEnum
from faslava.models import BaseModel
from faslava.core.utils import gettext_lazy as _


class BaseAlembicSchemaModel(BaseModel):
    # Define the almbc schema for child models:
    # __table_args__ = {"schema": "almbc"}  # Specify the schema
    pass


class TechnicalProperty(BaseAlembicSchemaModel, table=True):
    """Primary Product table."""

    __tablename__ = "technical_properties"

    id: Optional[int] = Field(primary_key=True, description=_("ID"))
    product_id: int = Field(description="Product ID", foreign_key="product.id")
    name: TechnicalPropertyEnum = Field(description=_("Name"))
    value: str = Field(description=_("Value"))


class Product(BaseAlembicSchemaModel, table=True):
    """Primary Product table."""

    __tablename__ = "product"

    id: Optional[int] = Field(primary_key=True, description=_("ID"))
    name: str = Field(max_length=256, description=_("Name"))
    price: Decimal = Field(decimal_places=2, max_digits=11, description=_("Price"))
    description: Optional[str] = Field(default="", description=_("Description"))
    technical_properties: str = Field(default="", description=_("Technical Properties"))
