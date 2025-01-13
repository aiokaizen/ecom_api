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
    technical_properties: dict


class ProductCreateSerializer(BaseSerializer):
    name: str
    price: float
    description: str | None = None
    technical_properties: dict | None = None
