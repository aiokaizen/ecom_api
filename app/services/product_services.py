from typing import Sequence, Tuple
from sqlalchemy.exc import NoResultFound
from sqlalchemy.sql import and_
from sqlmodel import Session, select
from app.models.models import Product
from faslava.config.database_manager import db_manager
from faslava.core.filters import Filter
from faslava.exceptions.exceptions import InvalidPaginationOffset
from faslava.logging.logging_manager import logger


def create_product(product: Product):
    try:
        with db_manager.session_scope() as session:
            logger.info(f"Insert product: {product}")
            session.add(product)
            session.commit()
            session.flush()
        return product
    except Exception as e:
        logger.error("Unexpected error:", e)


def get_product_with_id(session: Session, id: int) -> Product:
    try:
        logger.info(f"Select product with ID: {id}")
        statement = select(Product).where(Product.id == id)
        product = session.exec(statement).one()
        return product
    except NoResultFound:
        raise Product.no_result_found_exc()


def filter_products(
    session: Session,
    offset: int = 0,
    limit: int = 10,
    filters: Filter | None = None,
) -> Tuple[Sequence[Product], int]:
    """
    Filters product using the filters provided, while limiting the results using limit and offset.

    Args:
        session (Session): The database session.
        offset (int): The offset to skip before returning results.
        limit (int): The max amount of results to return
        filters (Optional[Filter]): Filter object defining how results should be filtered

    Raises:
        InvalidPaginationOffset if the offset is provided and the result is empty

    Returns:
        A tuple containing the list of products alongside the total number of products in the database.
    """
    logger.info(f"Filter products with the following filters: {filters}")

    # Change this method, get the length from db.
    total_items = len(session.exec(select(Product)).all())

    statement = (
        select(Product)
        .where(filters.build_filters() if filters else True)
        .offset(offset)
        .limit(limit)
    )
    result = session.exec(statement)
    products = result.all()

    if not products and offset > 0:
        raise InvalidPaginationOffset()

    return products, total_items
