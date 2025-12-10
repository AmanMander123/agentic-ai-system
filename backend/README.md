# Backend (FastAPI)

## Run locally
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000/health` to confirm the service is alive.

### Call the agent endpoint
```bash
curl -X POST http://127.0.0.1:8000/agent/query \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, agent!"}'
```

### Environment
- `GCP_PROJECT_ID` (required): project used to fetch secrets from Secret Manager.
- `OPENAI_SECRET_NAME` (optional, default `openai-api-key`): name of the secret in Secret Manager containing the OpenAI API key.
- `OPENAI_AGENT_ID` (optional): route calls to a pre-provisioned agent ID. If omitted, the endpoint will call the specified model directly.
- `OPENAI_MODEL` (optional): defaults to `gpt-4o-mini` when no agent ID is provided.

## Notes
- Keep secrets out of the repo. Configure environment variables locally and prefer a secret manager (e.g., Google Secret Manager) in non-local environments.
- The app is organized for growth: routers live under `app/api/routes`, and core settings/middleware can go under `app/core` as they are added.

## Secret Manager setup (local)
1) Authenticate and set ADC for local dev:
```bash
gcloud auth login
gcloud auth application-default login
gcloud config set project YOUR_GCP_PROJECT_ID
```
2) Enable Secret Manager if not already:
```bash
gcloud services enable secretmanager.googleapis.com
```
3) Create the secret (one-time) and add your key:
```bash
gcloud secrets create openai-api-key --replication-policy="automatic"
printf \"%s\" \"sk-...\" | gcloud secrets versions add openai-api-key --data-file=-
```
4) Export env so the app knows where to look:
```bash
export GCP_PROJECT_ID=YOUR_GCP_PROJECT_ID
# export OPENAI_SECRET_NAME=openai-api-key  # if you used a different name
```

## Secret Manager setup (Cloud Run)
- Deploy with a service account that has `Secret Manager Secret Accessor` on the OpenAI secret.
- Ensure the service account also has permission to run (e.g., Cloud Run Invoker as needed).
- Cloud Run uses its service account ADC automatically; no API key env var required—only `GCP_PROJECT_ID` (and optional `OPENAI_SECRET_NAME`).
