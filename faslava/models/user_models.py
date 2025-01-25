from typing import Dict, List, Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON, Boolean, String, Integer

from enums.enums import GenderEnum
from faslava.models.base_models import BaseModel


class BasePerson(BaseModel):
    __abstract__ = True

    first_name: Mapped[str] = mapped_column(String(64))
    last_name: Mapped[str] = mapped_column(String(64))
    full_name: Mapped[Optional[str]] = mapped_column(String(64))
    gender: Mapped[GenderEnum] = mapped_column(String(1))
    image_url: Mapped[Optional[str]] = mapped_column(String(512))
    geoip: Mapped[Optional[Dict]] = mapped_column(JSON(none_as_null=True))


class UserAccount(BasePerson):
    __tablename__ = "user_account"
    __display_name__ = "User"

    addresses: Mapped[List["Address"]] = relationship()

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, first_name={self.first_name!r}, last_name={self.last_name!r})"


class Address(BaseModel):
    __tablename__ = "address"
    __display_name__ = "Address"
    __mapper_args__ = {
        "polymorphic_identity": "address",
    }

    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey(UserAccount.id))
    email_address: Mapped[str] = mapped_column(String(64))
    email_address_verified: Mapped[bool] = mapped_column(Boolean)
    phone_number: Mapped[str] = mapped_column(
        String(19)
    )  # Max format: `(+212) 644 87 65 91`
    street: Mapped[str] = mapped_column(String(512))
    city: Mapped[str] = mapped_column(String(64))
    postal_code: Mapped[int] = mapped_column(Integer)
    user: Mapped[Optional[UserAccount]] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"
