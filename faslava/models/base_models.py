from datetime import datetime
from typing import Optional, Type

from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.sql import text
from sqlalchemy.types import DateTime

from faslava.core.utils import gettext_lazy as _
from faslava.exceptions.exceptions import BaseException

# class User(Base):
#     __tablename__ = "user_account"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(30))
#     fullname: Mapped[Optional[str]]
#     addresses: Mapped[List["Address"]] = relationship(back_populates="user")
#
#     def __repr__(self) -> str:
#         return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"
#
# class Address(Base):
#     __tablename__ = "address"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     email_address: Mapped[str]
#     user_id = mapped_column(ForeignKey("user_account.id"))
#     user: Mapped[User] = relationship(back_populates="addresses")
#
#     def __repr__(self) -> str:
#         return f"Address(id={self.id!r}, email_address={self.email_address!r})"


class BaseModel(DeclarativeBase):
    """BaseModel for all the database classes."""

    __exception__ = None

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(), server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(), default=None, server_onupdate=text("CURRENT_TIMESTAMP")
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(), default=None, server_onupdate=text("CURRENT_TIMESTAMP")
    )

    @classmethod
    def no_result_found_exc(cls, message: Optional[str] = None) -> Type[BaseException]:
        """
        Generates a dedicated NoResultFound exception.

        The generated class differenciates each model's NoResultFound exception, making it easier
        to target individual model exceptions.
        """
        if cls.__exception__:
            return cls.__exception__

        class TargetedNoResultFound(BaseException):
            def __init__(self, http_error_code: int = 404, **kwargs):
                exc_message = kwargs.get("message", message)
                if not exc_message:
                    model_name = getattr(cls, "__display_name__", cls.__name__)
                    exc_message = _(f"{model_name} does not exist.")

                super().__init__(
                    http_error_code=http_error_code, message=exc_message, **kwargs
                )

        cls.__exception__ = TargetedNoResultFound
        return TargetedNoResultFound
