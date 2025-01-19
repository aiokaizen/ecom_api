from collections.abc import Generator
from contextlib import contextmanager
from threading import Lock

from sqlmodel import Session, create_engine

from faslava.config.configuration import settings


class DatabaseManager:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        """Implement thread-safe singleton behavior."""

        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self, database_url):
        # Initialize the database engine and session maker only once
        if not hasattr(self, "_initialized"):
            self.engine = create_engine(database_url, echo=True)
            self._initialized = True

    @contextmanager
    def session_scope(self) -> Generator[Session]:
        """
        Provide a transactional scope for database operations.
        Automatically commits on success and rolls back on exceptions.
        Ensures the session is always closed at the end.
        """
        session = Session(self.engine)
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    # def create_tables(self):
    #     # Create all tables defined by SQLModel
    #     SQLModel.metadata.create_all(self.engine)


db_manager = DatabaseManager(settings.build_db_url())
