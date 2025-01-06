from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine
from sqlalchemy import Column, DateTime


class Hero(SQLModel, table=True):
    """Represents Hero class in DB."""

    __table_args__ = {"schema": "mk", "extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True)),
        default_factory=lambda: datetime.now(timezone.utc),
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), onupdate=lambda: datetime.now(timezone.utc)
        ),
        default_factory=lambda: datetime.now(timezone.utc),
    )


hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador", age=32)
hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)


db_url = "postgresql://user:pwd@host.com:5432/postgres"
engine = create_engine(db_url)


SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    session.add(hero_1)
    session.add(hero_2)
    session.add(hero_3)
    session.commit()
    session.flush()

    print("hero1 creation date:", hero_1.created_at)
    print("hero1 update date:", hero_1.updated_at)

    hero_1.age = 24
    session.add(hero_1)
    session.commit()
    session.flush()

    print("\nhero1 creation date:", hero_1.created_at)
    print("hero1 update date:", hero_1.updated_at)
