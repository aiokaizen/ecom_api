from fastapi import Query
from fastapi.routing import APIRouter

from app.serializers import product_serializers
from faslava.logging.logging_manager import logger
from faslava.config.database_manager import db_manager

from app.serializers import Product
from app.serializers.product_serializers import (
    ProductGetSerializer,
    ProductListSerializer,
)
from app.services.product_services import filter_products, get_product_with_id
from faslava.serializers.api_serializers import generate_paginated_response


router = APIRouter()

ProductPaginatedResponse = generate_paginated_response(ProductListSerializer)


@router.get("/", response_model=ProductPaginatedResponse)
async def list_products(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1),
):  # Query params
    try:
        with db_manager.session_scope() as session:
            products, total_count = filter_products(session, offset, limit)
            serialized_products = [
                ProductListSerializer(**product.model_dump()) for product in products
            ]
            return ProductPaginatedResponse(
                total_count=total_count,
                results=serialized_products,
            )
    except Exception as e:
        logger.error("Unexpected error:", e)
        raise e


@router.get("/{product_id}", response_model=ProductGetSerializer)
async def read_product(product_id: int):
    try:
        with db_manager.session_scope() as session:
            product = get_product_with_id(session, product_id)
            product_serializer = ProductGetSerializer(**product.model_dump())
            return product_serializer
    except Exception as e:
        logger.error("Unexpected error:", e)
        raise e


@router.post("/")
async def create_product(product: Product):
    product = await create_product(product)
    return product
