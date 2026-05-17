import hashlib
import hmac
import json
import httpx
import asyncio
from fastapi import APIRouter, Request, Header, BackgroundTasks
from app.services.ai_reviewer import review_code
from app.core.config import settings

router = APIRouter()

async def process_pr_review(pr_number: int, repo_name: str, pr_title: str, diff_url: str):
    try:
        # Fetch the diff
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            diff_response = await client.get(
                diff_url,
                headers={"Accept": "application/vnd.github.v3.diff"}
            )
            diff = diff_response.text

        # Get AI review
        review = review_code(diff, pr_title)
        print("AI Review Generated!")

        # Post comment on GitHub PR
        import os
        github_token = os.environ.get("GITHUB_TOKEN")
        if github_token:
            from github import Github
            g = Github(github_token)
            repo = g.get_repo(repo_name)
            pr = repo.get_pull(pr_number)
            pr.create_issue_comment(f"## 🤖 AI Code Review\n\n{review}")
            print(f"Comment posted on PR #{pr_number}!")

    except Exception as e:
        print(f"Review failed: {e}")

@router.post("/webhook/github")
async def github_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
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

            print(f"PR #{pr_number} received — starting background review...")

            # Respond instantly, process in background
            background_tasks.add_task(
                process_pr_review,
                pr_number, repo_name, pr_title, diff_url
            )

            return {"status": "received", "pr": pr_number}

    return {"status": "ignored", "event": x_github_event}