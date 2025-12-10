from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.services.agent_client import AgentClient, AgentClientError, get_agent_client

router = APIRouter()


class AgentQuery(BaseModel):
    message: str = Field(..., description="End-user prompt for the agent.")


@router.post(
    "/query",
    summary="Ask the agent a question",
    status_code=status.HTTP_200_OK,
)
async def query_agent(
    payload: AgentQuery, client: AgentClient = Depends(get_agent_client)
) -> dict:
    try:
        result = await client.respond(payload.message)
    except AgentClientError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)
        ) from exc
    except Exception as exc:  
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Agent call failed; see server logs.",
        ) from exc

    return {"status": "ok", "data": result}
