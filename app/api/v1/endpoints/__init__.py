from fastapi.routing import APIRouter

from .products import router as products_router


router = APIRouter(prefix="/v1")

# Products router
router.include_router(products_router, prefix="/products", tags=["products"])
