from fastapi import FastAPI

from app.api.routes import register_routes


def create_app() -> FastAPI:
    app = FastAPI(
        title="Agentic AI System",
        version="0.1.0",
        description="Backend API for the production-grade AI agent stack.",
    )

    register_routes(app)

    return app


app = create_app()
