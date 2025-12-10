from fastapi import APIRouter, FastAPI

from app.api.routes import agent, health


def register_routes(app: FastAPI) -> None:
    api_router = APIRouter()

    api_router.include_router(health.router, prefix="/health", tags=["health"])
    api_router.include_router(agent.router, prefix="/agent", tags=["agent"])

    app.include_router(api_router)
