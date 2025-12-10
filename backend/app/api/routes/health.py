from fastapi import APIRouter

router = APIRouter()


@router.get("/", summary="Health check")
async def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "agentic-ai-system",
        "message": "Backend is up. Auth and tooling to follow.",
    }
