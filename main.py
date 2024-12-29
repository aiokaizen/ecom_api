from typing import List
from fastapi import FastAPI
import json

from app.serializers import Product
from app.serializers.product_serializers import ProductListSerializer
from app.services.product_services import filter_products, get_product
from faslava.logging.logging_manager import logger

app = FastAPI()


mock_data = None
with open("seeding_data.json", "r") as f:
    mock_data = json.load(f)


@app.get("/")
async def health_check():
    return {"status": "OK"}


@app.get("/products/", response_model=List[Product])
async def list_products(skip: int = 0, limit: int = 10):  # Query params
    try:
        print("skip:", skip, "| limit:", limit)
        products = filter_products()
        return products
    except Exception as e:
        logger.error("Unexpected error:", e)


@app.get("/products/{product_id}")
async def read_product(product_id: int):
    try:
        product = get_product(product_id)
        return product
    except Exception as e:
        logger.error("Unexpected error:", e)
        raise e


@app.post("/products/")
async def create_product(product: Product):
    product = await create_product(product)
    return product
