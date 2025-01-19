from fastapi import HTTPException, Query, status as http_status
from fastapi.routing import APIRouter

from faslava.core.messages import UNKNOWN_ERROR_MESSAGE
from faslava.enums.enums import APIResponseStatusEnum
from faslava.exceptions.exceptions import InvalidPaginationOffset
from faslava.logging.logging_manager import logger
from faslava.config.database_manager import db_manager
from faslava.core.utils import gettext_lazy as _
from faslava.serializers.api_serializers import APIResponse, generate_paginated_response

from app.models import Product
from app.serializers.product_serializers import (
    ProductCreateUpdateSerializer,
    ProductGetSerializer,
    ProductListSerializer,
)
from app.services.product_services import (
    create_product,
    delete_product,
    filter_products,
    get_product_with_id,
    update_product,
)


router = APIRouter()

ProductPaginatedResponse = generate_paginated_response(ProductListSerializer)


@router.get("/", response_model=ProductPaginatedResponse)
async def product_list_endpoint(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1),
):
    with db_manager.session_scope() as session:
        products, total_count = filter_products(session, offset, limit)
        serialized_products = [
            ProductListSerializer(**product.model_dump()) for product in products
        ]
        return ProductPaginatedResponse(
            total_count=total_count,
            offset=offset,
            limit=limit,
            results=serialized_products,
        )


@router.post("/", status_code=201, response_model=APIResponse)
async def product_create_endpoint(product_data: ProductCreateUpdateSerializer):
    try:
        with db_manager.session_scope() as session:
            product = create_product(session, product_data)
            return APIResponse(
                status=APIResponseStatusEnum.SUCCESS,
                message=_("Product created successfully."),
                obj=ProductGetSerializer(**product.model_dump()),
            )
    except InvalidPaginationOffset as e:
        raise HTTPException(
            status_code=e.http_error_code,
            detail=APIResponse(
                status=APIResponseStatusEnum.ERROR, message=e.message
            ).model_dump(),
        )


@router.get("/{product_id}", response_model=ProductGetSerializer)
async def product_retrieve_endpoint(product_id: int):
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


@router.put(
    "/{product_id}",
    status_code=200,
    response_model=APIResponse,
    responses={
        200: {
            "model": APIResponse,
            "description": "Product updated successfully.",
        },
        500: {
            "model": APIResponse,
            "description": UNKNOWN_ERROR_MESSAGE,
        },
    },
)
async def product_update_endpoint(
    product_id: int, product_data: ProductCreateUpdateSerializer
):
    try:
        with db_manager.session_scope() as session:
            product = update_product(
                session, product_id=product_id, product_data=product_data
            )
            return APIResponse(
                status=APIResponseStatusEnum.SUCCESS,
                message=_("Product updated successfully."),
                obj=ProductGetSerializer(**product.model_dump()),
            )
    except Product.no_result_found_exc() as e:
        raise HTTPException(
            status_code=e.http_error_code,
            detail=APIResponse(
                status=APIResponseStatusEnum.ERROR,
                message=e.message,
            ).model_dump(),
        )


@router.delete(
    "/{product_id}",
    status_code=200,
    response_model=APIResponse,
    responses={
        200: {
            "model": APIResponse,
            "description": "Product deleted successfully.",
        },
        500: {
            "model": APIResponse,
            "description": UNKNOWN_ERROR_MESSAGE,
        },
    },
)
async def product_delete_endpoint(product_id: int):
    try:
        with db_manager.session_scope() as session:
            delete_product(session, product_id=product_id)
            return APIResponse(
                status=APIResponseStatusEnum.SUCCESS,
                message=_("Product deleted successfully."),
            )
    except Product.no_result_found_exc() as e:
        raise HTTPException(
            status_code=e.http_error_code,
            detail=APIResponse(
                status=APIResponseStatusEnum.ERROR,
                message=e.message,
            ).model_dump(),
        )
