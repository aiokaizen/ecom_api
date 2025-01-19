from typing import Any, List, Type
from faslava.enums.enums import APIResponseStatusEnum
from faslava.serializers.serializers import BaseSerializer


class APIResponse(BaseSerializer):
    """Serves as a response serializer for most API operations."""

    status: APIResponseStatusEnum
    message: str
    obj: Any = None


def generate_paginated_response(serializer: Type[BaseSerializer]):
    """
    Generates a paginated response class dedicated for the provided serializer and returs it.

    Args:
        serializer (Class inheriting from BaseSerializer): The serializer to generate the paginated response for.

    Usage:
        >>>

    Returns:
        DedicatedPaginatedResponse with the provided serializer as a result.
    """

    class DedicatedPaginatedResponse(BaseSerializer):
        total_count: int
        offset: int
        limit: int
        results: List[serializer]

    return DedicatedPaginatedResponse
