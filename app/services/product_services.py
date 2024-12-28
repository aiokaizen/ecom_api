from typing import List, Sequence
from sqlalchemy.sql import and_
from sqlmodel import select
from app.models.models import Product
from faslava.config.database_manager import db_manager
from faslava.core.filters import Filter
from faslava.logging.logging_manager import logger


async def create_product(product):
    try:
        with db_manager.session_scope() as session:
            session.add(product)
    except Exception as e:
        logger.error("Unexpected error:", e)


def get_product(id: int) -> Product | None:
    try:
        with db_manager.session_scope() as session:
            statement = select(Product).where(Product.id == id)
            product = session.exec(statement).first()
            return product
    except Exception as e:
        logger.error("Unexpected error:", e)
        raise e



def filter_products(filters: Filter | None = None) -> Sequence[Product]:
    try:
        with db_manager.session_scope() as session:
            statement = select(Product).where(filters.build_filters() if filters else True)
            products = session.exec(statement).all()
            return products
    except Exception as e:
        logger.error("Unexpected error:", e)
        raise e

