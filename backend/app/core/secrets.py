from __future__ import annotations

from functools import lru_cache

from google.cloud import secretmanager


class SecretManagerError(Exception):
    """Raised when a secret cannot be retrieved."""


@lru_cache
def _get_secret_client() -> secretmanager.SecretManagerServiceClient:
    return secretmanager.SecretManagerServiceClient()


def fetch_secret(
    *, project_id: str, secret_name: str, version: str = "latest"
) -> str:
    """
    Retrieve a secret value from Google Secret Manager.

    The caller must have access via ADC (local: `gcloud auth application-default login`,
    Cloud Run: service account with Secret Manager Accessor role on the secret).
    """
    client = _get_secret_client()
    secret_path = client.secret_version_path(project_id, secret_name, version)

    try:
        response = client.access_secret_version(name=secret_path)
    except Exception as exc:  # pragma: no cover - depends on GCP environment
        raise SecretManagerError(f"Failed to access secret {secret_name}: {exc}") from exc

    payload = response.payload.data.decode("utf-8")
    if not payload:
        raise SecretManagerError(f"Secret {secret_name} is empty.")

    return payload
