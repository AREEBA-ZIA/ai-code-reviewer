from google import genai
import os

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def review_code(diff: str, pr_title: str) -> str:
    prompt = f"""You are an expert code reviewer. Review this GitHub Pull Request and provide helpful feedback.

PR Title: {pr_title}

Code Changes (diff):
{diff}

Provide a structured review with:
1. **Summary** - What this PR does
2. **Issues Found** - Bugs, security issues, performance problems
3. **Suggestions** - Improvements and best practices
4. **Overall Assessment** - Approve / Request Changes

Be specific and helpful. Format nicely with markdown."""

    response = client.models.generate_content(
model="gemini-2.0-flash",       
contents=prompt
    )
    return response.text