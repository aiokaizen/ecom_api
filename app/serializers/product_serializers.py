from faslava.serializers.serializers import (
    BaseCreateUpdateSerializer,
    BaseORMSerializer,
)


class ProductSerializer(BaseORMSerializer):
    id: int
    name: str
    price: float
    description: str | None = None
    technical_properties: dict


class ProductListSerializer(BaseORMSerializer):
    id: int
    name: str
    price: float


class ProductCreateUpdateSerializer(BaseCreateUpdateSerializer):
    name: str
    price: float
    description: str | None = None
    technical_properties: dict | None = None
