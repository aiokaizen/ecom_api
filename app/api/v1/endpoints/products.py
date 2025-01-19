from fastapi import HTTPException, Query, status as http_status
from fastapi.routing import APIRouter

from faslava.enums.enums import APIResponseStatusEnum
from faslava.logging.logging_manager import logger
from faslava.config.database_manager import db_manager
from faslava.core.utils import gettext_lazy as _
from faslava.serializers.api_serializers import APIResponse, generate_paginated_response

from app.models import Product
from app.serializers.product_serializers import (
    ProductGetSerializer,
    ProductListSerializer,
)
from app.services.product_services import filter_products, get_product_with_id


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
    except Product.no_result_found_exc() as e:
        raise HTTPException(
            status_code=e.http_error_code,
            detail=APIResponse(
                status=APIResponseStatusEnum.ERROR,
                message=e.message,
            ).model_dump(),
        )
    except Exception as e:
        logger.error("Unexpected error:", e)
        raise e


@router.post("/")
async def create_product(product: Product):
    product = await create_product(product)
    return product
