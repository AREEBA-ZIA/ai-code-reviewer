import hashlib
import hmac
import json
from fastapi import APIRouter, Request, HTTPException, Header
from app.core.config import settings

router = APIRouter()

def verify_webhook_signature(payload: bytes, signature: str) -> bool:
    if not signature:
        return False
    expected = hmac.new(
        settings.GITHUB_WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    expected_header = f"sha256={expected}"
    return hmac.compare_digest(expected_header, signature)

@router.post("/webhook/github")
async def github_webhook(
    request: Request,
    x_github_event: str = Header(None),
    x_hub_signature_256: str = Header(None)
):
    payload = await request.body()

    if not verify_webhook_signature(payload, x_hub_signature_256):
        raise HTTPException(status_code=401, detail="Invalid signature")

    data = json.loads(payload)

    if x_github_event == "pull_request":
        action = data.get("action")
        if action in ["opened", "synchronize", "reopened"]:
            pr_number = data["pull_request"]["number"]
            repo_name = data["repository"]["full_name"]
            pr_title = data["pull_request"]["title"]
            print(f"New PR #{pr_number} in {repo_name}: {pr_title}")
            return {
                "status": "received",
                "pr": pr_number,
                "repo": repo_name,
                "action": action
            }

    return {"status": "ignored", "event": x_github_event}