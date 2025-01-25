from threading import Lock

from sqlalchemy import create_engine, event, text

from faslava.config.configuration import settings
from faslava.logging import logger


class DatabaseManager:
    _instance = None
    _lock = Lock()

    def __new__(cls, **kwargs):
        """Implement thread-safe singleton behavior."""

        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self, *, database_url: str):
        # Initialize the database engine and session maker only once
        if not getattr(self, "_initialized", False):
            self._engine = create_engine(database_url, echo=settings.DEBUG)
            self._initialized = True

    def get_engine(self):
        return self._engine


_db_manager = DatabaseManager(database_url=settings.build_db_url())
engine = _db_manager.get_engine()


@event.listens_for(engine, "engine_connect")
def set_search_path(connection, branch):
    if not settings.CUSTOM_SCHEMA:
        return

    logger.info(f"Changing search path to: {settings.CUSTOM_SCHEMA}")
    change_schema_query = text(f'SET search_path TO "{settings.CUSTOM_SCHEMA}"')
    connection.execute(change_schema_query)
    connection.commit()
    logger.info("Search path is set successfully.")
