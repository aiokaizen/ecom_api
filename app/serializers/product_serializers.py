from faslava.serializers.serializers import (
    BaseCreateUpdateSerializer,
    BaseORMSerializer,
)


class ProductSerializer(BaseORMSerializer):
    id: int
    name: str
    price: float
    description: str | None = None
    custom_properties: dict


class ProductListSerializer(BaseORMSerializer):
    id: int
    name: str
    price: float


class ProductCreateUpdateSerializer(BaseCreateUpdateSerializer):
    name: str
    price: float
    description: str | None = None
    custom_properties: dict | None = None
