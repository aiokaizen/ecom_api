from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel

from faslava.core.utils import gettext_lazy as _


class BaseModel(SQLModel):
    """BaseModel for all the database classes."""

    pass

    created_at: datetime = Field(
        default_factory=(lambda: datetime.now(timezone.utc)),
        description=_("Created at"),
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        description=_("Updated at"),
        # sa_column=Column(DateTime(), onupdate=func.now()),  # Find out why this does not work!!
    )
    deleted_at: Optional[datetime] = Field(default=None, description=_("Deleted at"))
