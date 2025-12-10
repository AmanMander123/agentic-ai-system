from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import Depends

from app.core.config import Settings, get_settings
from app.core.secrets import SecretManagerError, fetch_secret


class AgentClientError(Exception):
    """Raised when the agent client cannot fulfill a request."""


class AgentClient:
    def __init__(self, settings: Settings) -> None:
        if not settings.gcp_project_id:
            raise AgentClientError("GCP_PROJECT_ID is not configured.")

        try:
            api_key = fetch_secret(
                project_id=settings.gcp_project_id,
                secret_name=settings.openai_secret_name,
            )
        except SecretManagerError as exc:
            raise AgentClientError(str(exc)) from exc

        # Import lazily to keep module import light during app startup.
        from openai import AsyncOpenAI  

        self.client = AsyncOpenAI(api_key=api_key, max_retries=2)
        self.agent_id = settings.openai_agent_id
        self.model = settings.openai_model

    async def respond(self, message: str) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"input": message}

        if self.agent_id:
            payload["agent_id"] = self.agent_id
        else:
            payload["model"] = self.model

        response = await self.client.responses.create(**payload)
        return self._extract_text_response(response)

    def _extract_text_response(self, response: Any) -> Dict[str, Any]:
        # Attempt to extract the first text output. If the structure changes,
        # return the raw payload for transparency.
        output_blocks = getattr(response, "output", None)
        if output_blocks:
            for block in output_blocks:
                content = getattr(block, "content", None)
                if not content:
                    continue
                for item in content:
                    text_value: Optional[str] = getattr(item, "text", None) or getattr(
                        item, "value", None
                    )
                    if text_value:
                        return {"output": text_value}

        if hasattr(response, "model_dump"):
            return {"output": response.model_dump()}

        return {"output": str(response)}


def get_agent_client(settings: Settings = Depends(get_settings)) -> AgentClient:
    return AgentClient(settings)
