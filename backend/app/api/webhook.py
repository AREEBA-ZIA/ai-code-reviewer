import hashlib
import hmac
import json
import httpx
from fastapi import APIRouter, Request, HTTPException, Header
from app.core.config import settings
from app.services.ai_reviewer import review_code
from github import Github

router = APIRouter()

def verify_webhook_signature(payload: bytes, signature: str) -> bool:
    if not signature:
        return False
    mac = hmac.new(
        settings.GITHUB_WEBHOOK_SECRET.encode('utf-8'),
        msg=payload,
        digestmod=hashlib.sha256
    )
    expected_header = f"sha256={mac.hexdigest()}"
    return hmac.compare_digest(expected_header, signature)

@router.post("/webhook/github")
async def github_webhook(
    request: Request,
    x_github_event: str = Header(None),
    x_hub_signature_256: str = Header(None)
):
    payload = await request.body()

    data = json.loads(payload)

    if x_github_event == "pull_request":
        action = data.get("action")
        if action in ["opened", "synchronize", "reopened"]:
            pr_number = data["pull_request"]["number"]
            repo_name = data["repository"]["full_name"]
            pr_title = data["pull_request"]["title"]
            diff_url = data["pull_request"]["diff_url"]

            print(f"Reviewing PR #{pr_number} in {repo_name}: {pr_title}")

            # Fetch the diff
            async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
                diff_response = await client.get(
                    diff_url,
                    headers={"Accept": "application/vnd.github.v3.diff"}
                )
                diff = diff_response.text

            # Get AI review
            try:
                review = review_code(diff, pr_title)
                print("AI Review Generated!")

                # Post comment on GitHub PR
                import os
                github_token = os.environ.get("GITHUB_TOKEN")
                if github_token:
                    g = Github(github_token)
                    repo = g.get_repo(repo_name)
                    pr = repo.get_pull(pr_number)
                    pr.create_issue_comment(f"## 🤖 AI Code Review\n\n{review}")
                    print(f"Comment posted on PR #{pr_number}!")

            except Exception as e:
                print(f"AI Review failed: {e}")
                review = "AI review temporarily unavailable."

            return {
                "status": "reviewed",
                "pr": pr_number,
                "repo": repo_name
            }

    return {"status": "ignored", "event": x_github_event}