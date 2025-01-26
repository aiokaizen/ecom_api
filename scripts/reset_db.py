from sqlalchemy import delete

from faslava.config.database_manager import engine
from faslava.logging import logger
from faslava.models.user_models import Address, UserAccount

from app.models.product_models import Category, Customer, Order, Product, Tag


def reset_db():
    logger.info("Reseting database...")
    with engine.begin() as conn:
        conn.execute(delete(Tag))
        conn.execute(delete(Product))
        conn.execute(delete(Category))
        conn.execute(delete(Order))
        conn.execute(delete(Customer))
        conn.execute(delete(Address))
        conn.execute(delete(UserAccount))
