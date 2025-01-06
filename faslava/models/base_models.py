from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel, Column, DateTime, text, func

from faslava.core.utils import gettext_lazy as _


class BaseModel(SQLModel):
    """BaseModel for all the database classes."""

    created_at: datetime = Field(
        sa_column=lambda: Column(
            DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP")
        ),
        description=_("Created at"),
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        description=_("Updated at"),
        sa_column=lambda: Column(
            DateTime(timezone=True),
            onupdate=func.now(),
            server_onupdate=text("CURRENT_TIMESTAMP"),
        ),
    )
    deleted_at: Optional[datetime] = Field(
        default=None,
        description=_("Deleted at"),
        sa_column=lambda: Column(DateTime(timezone=True)),
    )
