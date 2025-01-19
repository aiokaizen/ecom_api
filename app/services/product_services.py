from typing import Sequence, Tuple
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select
from app.models.models import Product
from app.serializers.product_serializers import ProductCreateUpdateSerializer
from faslava.core.filters import Filter
from faslava.exceptions.exceptions import InvalidPaginationOffset
from faslava.logging.logging_manager import logger


def get_product_with_id(session: Session, id: int) -> Product:
    """
    Fetche a product from the datasbase using it's ID.

    Args:
        session (Session): The database session
        product_id (int): The product id used to fetch the database.

    Returns:
        Product: The retrieved product.

    Raises:
        Product.no_result_found_exc(): if no product is found with the provided ID.
    """
    try:
        logger.info(f"Select product with ID: {id}")
        statement = select(Product).where(Product.id == id)
        result = session.exec(statement)
        product = result.one()
        return product
    except NoResultFound:
        raise Product.no_result_found_exc()


def create_product(session: Session, product_data: ProductCreateUpdateSerializer):
    """
    Create a new product in the datasbase.

    Args:
        session (Session): The database session
        product_data (ProductCreateUpdateSerializer): The product data to insert into the database.

    Returns:
        Product: The newly created product.
    """
    logger.info(f"Insert product: {product_data}")
    product = Product(**product_data.model_dump())
    session.add(product)
    session.flush()
    return product


def update_product(
    session: Session, *, product_id: int, product_data: ProductCreateUpdateSerializer
):
    """
    Update a product in the datasbase.

    Args:
        session (Session): The database session
        product_id (int): The product id that should be updated in the database.
        product_data (ProductCreateUpdateSerializer): The product data to update in the database.

    Raises:
        Product.no_result_found_exc(): if no product is found with the provided ID.

    Returns:
        Product: The product with the updated data
    """
    try:
        logger.info(f"Update product {product_id} with data: {product_data}")
        product = Product(**product_data.model_dump())
        statement = select(Product).where(Product.id == product_id)
        result = session.exec(statement)
        product = result.one()

        for name, value in product_data.model_dump().items():
            setattr(product, name, value)

        session.add(product)
        session.flush()
        return product
    except NoResultFound:
        raise Product.no_result_found_exc()


def delete_product(session: Session, *, product_id: int):
    """
    Delete a product from the datasbase.

    Args:
        session (Session): The database session
        product_id (int): The product id that should be deleted from the database.

    Raises:
        Product.no_result_found_exc(): if no product is found with the provided ID.
    """
    try:
        logger.info(f"Delete product {product_id}.")
        statement = select(Product).where(Product.id == product_id)
        result = session.exec(statement)
        product = result.one()
        session.delete(product)
        session.flush()
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
