from datetime import datetime
from typing import Optional, Type
from sqlmodel import Field, SQLModel, DateTime, text

from faslava.core.utils import gettext_lazy as _
from faslava.exceptions.exceptions import BaseException


class BaseModel(SQLModel):
    """BaseModel for all the database classes."""

    __exception__ = None

    created_at: datetime = Field(
        # default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime,
        sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")},
        description=_("Created at"),
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        description=_("Updated at"),
        sa_type=DateTime,
        sa_column_kwargs={"server_onupdate": text("CURRENT_TIMESTAMP")},
    )
    deleted_at: Optional[datetime] = Field(
        default=None,
        description=_("Deleted at"),
        sa_type=DateTime,
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
