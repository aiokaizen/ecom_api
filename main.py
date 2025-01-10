from fastapi import FastAPI

from faslava.middlewares.middleware_manager import inject_middlewares

from app.api import router as api_router

app = FastAPI()

# Inject middlewares
inject_middlewares(app)

# Include API routers.
app.include_router(api_router)


@app.get("/")
async def health_check():
    return {"status": "OK"}
