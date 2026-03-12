from fastapi import FastAPI

from app.api.routes import router
from app.core.config import settings
from app.core.database import Base, engine


def create_app() -> FastAPI:
    Base.metadata.create_all(bind=engine)

    app = FastAPI(title=settings.app_name, version=settings.app_version)
    app.include_router(router)
    return app


app = create_app()
