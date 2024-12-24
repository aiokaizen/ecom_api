from pydantic import BaseModel



class Product(BaseModel):
    id: int
    name: str
    price: float
    description: str | None = None
    technical_properties: dict
