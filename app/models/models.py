from sqlmodel import Field, Session, SQLModel
from typing import Optional
from decimal import Decimal

from enums.enums import TechnicalPropertyEnum
from faslava.models import BaseModel
from faslava.core.utils import gettext_lazy as _


class TechnicalProperty(BaseModel, table=True):
    """Primary Product table."""

    __tablename__ = "technical_properties"

    id: Optional[int] = Field(primary_key=True, description=_("ID"))
    product_id: int = Field()
    name: TechnicalPropertyEnum = Field(description=_("Name"))
    value: str = Field(description=_("Value"))


class Product(BaseModel, table=True):
    """Primary Product table."""

    __tablename__ = "product"

    id: Optional[int] = Field(primary_key=True, description=_("ID"))
    name: str = Field(max_length=256, description=_("Name"))
    price: Decimal = Field(decimal_places=2, max_digits=11, description=_("Price"))
    description: Optional[str] = Field(default="", description=_("Description"))
    technical_properties: str = Field(
        default="", description=_("Technical Properties")
    )
