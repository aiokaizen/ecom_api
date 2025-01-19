from faslava.serializers.serializers import BaseSerializer


class ProductListSerializer(BaseSerializer):
    id: int
    name: str
    price: float


class ProductGetSerializer(BaseSerializer):
    id: int
    name: str
    price: float
    description: str | None = None
    technical_properties: dict


class ProductCreateUpdateSerializer(BaseSerializer):
    name: str
    price: float
    description: str | None = None
    technical_properties: dict | None = None
