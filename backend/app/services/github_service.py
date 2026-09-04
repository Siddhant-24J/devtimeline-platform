import httpx
from typing import Optional, List, Dict, Any
from app.core.config import settings

GITHUB_OAUTH_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
GITHUB_OAUTH_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_API_BASE_URL = "https://api.github.com"

def get_github_oauth_url(redirect_uri: Optional[str] = None) -> str:
    """Generates GitHub OAuth login authorization URL."""
    client_id = settings.GITHUB_CLIENT_ID or "demo_client_id"
    scope = "repo,user:email,workflow"
    url = f"{GITHUB_OAUTH_AUTHORIZE_URL}?client_id={client_id}&scope={scope}"
    if redirect_uri:
        url += f"&redirect_uri={redirect_uri}"
    return url

async def exchange_code_for_token(code: str) -> Optional[str]:
    """Exchanges authorization code for GitHub access token."""
    if not settings.GITHUB_CLIENT_ID or not settings.GITHUB_CLIENT_SECRET:
        # Fallback for development testing
        return "demo_access_token_gho_12345"

    headers = {"Accept": "application/json"}
    data = {
        "client_id": settings.GITHUB_CLIENT_ID,
        "client_secret": settings.GITHUB_CLIENT_SECRET,
        "code": code
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(GITHUB_OAUTH_TOKEN_URL, headers=headers, data=data)
        if response.status_code == 200:
            token_data = response.json()
            return token_data.get("access_token")
    return None

async def get_authenticated_github_user(token: str) -> Dict[str, Any]:
    """Fetches authenticated GitHub user profile."""
    if token.startswith("demo_"):
        return {
            "id": "12345678",
            "login": "demo_developer",
            "email": "developer@devtimeline.io",
            "avatar_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150"
        }

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{GITHUB_API_BASE_URL}/user", headers=headers)
        if response.status_code == 200:
            return response.json()
    return {}

async def list_github_repositories(token: str) -> List[Dict[str, Any]]:
    """Fetches user repositories from GitHub API."""
    if token.startswith("demo_"):
        return [
            {"id": 101, "name": "personal-portfolio", "full_name": "demo_developer/personal-portfolio", "private": False, "language": "TypeScript", "stargazers_count": 14},
            {"id": 102, "name": "ecommerce-platform", "full_name": "demo_developer/ecommerce-platform", "private": True, "language": "Python", "stargazers_count": 32},
            {"id": 103, "name": "ai-chatbot-platform", "full_name": "demo_developer/ai-chatbot-platform", "private": False, "language": "Python", "stargazers_count": 89},
            {"id": 104, "name": "intrusion-detection-system", "full_name": "demo_developer/intrusion-detection-system", "private": True, "language": "C++", "stargazers_count": 5}
        ]

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{GITHUB_API_BASE_URL}/user/repos?sort=updated&per_page=50", headers=headers)
        if response.status_code == 200:
            repos = response.json()
            return [
                {
                    "id": repo["id"],
                    "name": repo["name"],
                    "full_name": repo["full_name"],
                    "private": repo["private"],
                    "language": repo.get("language") or "Code",
                    "stargazers_count": repo.get("stargazers_count", 0)
                }
                for repo in repos
            ]
    return []
