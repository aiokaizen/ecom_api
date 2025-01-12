from app.models.models import Product
from faslava.serializers.serializers import BaseSerializer


class ProductListSerializer(BaseSerializer):
    id: int
    name: str
    price: float
    description: str | None = None


class ProductGetSerializer(BaseSerializer):
    id: int
    name: str
    price: float
    description: str | None = None
    # technical_properties: dict
    technical_properties: str


class ProductCreateSerializer(BaseSerializer):
    _model = Product

    name: str
    price: float
    description: str | None = None
    technical_properties: dict
