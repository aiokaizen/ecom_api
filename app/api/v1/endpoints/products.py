from typing import List

from fastapi.routing import APIRouter

from faslava.logging.logging_manager import logger

from app.serializers import Product
from app.serializers.product_serializers import ProductListSerializer
from app.services.product_services import filter_products, get_product


router = APIRouter()


@router.get("/", response_model=List[Product])
async def list_products(skip: int = 0, limit: int = 10):  # Query params
    try:
        products = filter_products()
        return products
    except Exception as e:
        logger.error("Unexpected error:", e)


@router.get("/{product_id}")
async def read_product(product_id: int):
    try:
        product = get_product(product_id)
        return product
    except Exception as e:
        logger.error("Unexpected error:", e)
        raise e


@router.post("/")
async def create_product(product: Product):
    product = await create_product(product)
    return product
