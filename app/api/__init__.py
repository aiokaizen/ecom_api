from fastapi.routing import APIRouter

from app.api.v1.endpoints import router as v1_router

router = APIRouter(prefix="/api")

# API v1 router
router.include_router(v1_router)
