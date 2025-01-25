from sqlalchemy import delete

from faslava.config.database_manager import engine
from faslava.logging import logger
from faslava.models.user_models import UserAccount

from app.models.product_models import Category, Product


def reset_db():
    logger.info("Reseting database...")
    with engine.begin() as conn:
        conn.execute(delete(Product))
        conn.execute(delete(Category))
        conn.execute(delete(UserAccount))
