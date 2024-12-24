from fastapi import FastAPI
import json

from app.serializers import Product

app = FastAPI()


mock_data = None
with open("data.json", "r") as f:
    mock_data = json.load(f)


@app.get("/")
async def health_check():
    return {"status": "OK"}


@app.get("/products/")
async def list_products(skip: int = 0, limit: int = 10):  # Query params
    mock_data_count = len(mock_data)
    limit = limit if limit <= mock_data_count else mock_data_count
    try:
        return mock_data[skip : skip + limit]
    except IndexError:
        return mock_data[:limit]


@app.get("/products/{product_id}")
async def read_product(product_id: int):
    try:
        product = [p for p in mock_data if p["id"] == product_id][0]
    except IndexError:
        return {"ERROR! Product not found."}
    return product


@app.post("/products/")
async def create_item(product: Product):
    mock_data.append(product.model_dump())
    return product


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
