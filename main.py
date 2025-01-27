from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse

from faslava.core.utils import save_uploaded_file
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


@app.post("/user-upload")
async def upload_file(file: UploadFile):
    if not file.size:
        return "Invalid file!"
    try:
        filename = await save_uploaded_file(file, batch_size=10000)
        return {"filesize": file.size, "filename": filename}
    finally:
        await file.close()


@app.get(
    "/user-upload/preview/{filename}",
    responses={
        200: {
            # "content": {"image/png": {}},
            "content": {"application/pdf": {}},
            "description": "Return PDF file",
        }
    },
)
async def read_item(filename: str):
    filepath = f"user_upload/{filename}"
    # return FileResponse(filepath, media_type="image/png")
    return FileResponse(filepath, media_type="application/pdf")
