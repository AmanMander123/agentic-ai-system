from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    gcp_project_id: str = Field(
        ...,
        env="GCP_PROJECT_ID",
        description="GCP project used for fetching secrets via Secret Manager.",
    )
    openai_secret_name: str = Field(
        default="openai-api-key",
        env="OPENAI_SECRET_NAME",
        description="Secret name in Secret Manager that stores the OpenAI API key.",
    )
    openai_agent_id: Optional[str] = Field(
        default=None,
        env="OPENAI_AGENT_ID",
        description="Existing agent ID to route requests to. If not set, the model is used directly.",
    )
    openai_model: str = Field(
        default="gpt-4o-mini",
        env="OPENAI_MODEL",
        description="Model used when creating ad-hoc responses without a pre-configured agent.",
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
