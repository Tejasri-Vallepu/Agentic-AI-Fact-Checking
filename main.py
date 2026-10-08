from fastapi import FastAPI

from app.api.routes import router
from app.core.config import settings


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": settings.APP_NAME,
        "status": "running",
    }
