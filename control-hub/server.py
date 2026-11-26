"""Local MCP adapter for a single, explicitly configured Vedra GitHub repository.

Run over stdio. Never expose this process through an unauthenticated network bridge.
"""
from __future__ import annotations

import base64
import os
import re
from typing import Any
from urllib.parse import quote

import httpx
from mcp.server.fastmcp import FastMCP

REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "rahulrankesh/ai-portfolio")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
API = "https://api.github.com"
BRANCH_PREFIXES = ("ai/", "control-hub/")
MAX_FILE_BYTES = 500_000

mcp = FastMCP("vedra-control-hub")


class GitHubError(RuntimeError):
    pass


def _headers() -> dict[str, str]:
    if not TOKEN:
        raise GitHubError("GITHUB_TOKEN is not configured in the server environment.")
    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def _request(method: str, path: str, **kwargs: Any) -> Any:
    with httpx.Client(timeout=25.0, follow_redirects=False) as client:
        response = client.request(method, f"{API}{path}", headers=_headers(), **kwargs)
    if response.status_code >= 400:
        # Do not surface request headers or token values in error messages.
        raise GitHubError(f"GitHub API returned HTTP {response.status_code}: {response.text[:500]}")
    if not response.content:
        return {}
    return response.json()


def _repo_path(suffix: str = "") -> str:
    owner, sep, name = REPOSITORY.partition("/")
    if not sep or not owner or not name or "/" in name:
        raise GitHubError("GITHUB_REPOSITORY must be owner/repository.")
    return f"/repos/{quote(owner)}/{quote(name)}{suffix}"


def _branch_ok(branch: str) -> bool:
    return bool(branch) and not branch.startswith("-") and any(branch.startswith(p) for p in BRANCH_PREFIXES)


def _path_ok(path: str) -> bool:
    if not path or path.startswith("/") or ".." in path.split("/") or "\\x00" in path:
        return False
    parts = path.lower().split("/")
    name = parts[-1]
    if name == ".env" or (name.startswith(".env.") and name != ".env.example"):
        return False
    if name.endswith((".pem", ".key", ".p12", ".pfx")) or name in {"id_rsa", "id_ed25519", "credentials.json"}:
        return False
    if any(part in {".ssh", "secrets", "credentials"} for part in parts):
        return False
    return True


@mcp.tool()
def repo_overview() -> dict[str, Any]:
    """Return safe metadata for the configured Vedra repository."""
    data = _request("GET", _repo_path())
    return {
        "repository": data.get("full_name"),
        "private": data.get("private"),
        "default_branch": data.get("default_branch"),
        "html_url": data.get("html_url"),
        "permissions": data.get("permissions"),
    }


@mcp.tool()
def read_repo_file(path: str, branch: str = "") -> dict[str, str]:
    """Read a text file from the configured repository. Never returns secret values from GitHub Actions."""
    if path.startswith("/") or ".." in path.split("/") or "\x00" in path:
        raise ValueError("Unsafe repository path.")
    ref = f"?ref={quote(branch)}" if branch else ""
    data = _request("GET", _repo_path(f"/contents/{quote(path, safe='/')}") + ref)
    if data.get("type") != "file":
        raise ValueError("Requested path is not a file.")
    raw = base64.b64decode(data.get("content", ""))
    if len(raw) > MAX_FILE_BYTES:
        raise ValueError("File exceeds the 500 KB read limit.")
    try:
        content = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Only UTF-8 text files are supported.") from exc
    return {"path": path, "sha": data["sha"], "content": content}


@mcp.tool()
def create_feature_branch(branch: str) -> dict[str, str]:
    """Create an ai/* or control-hub/* branch from the repository default branch."""
    if not _branch_ok(branch) or re.search(r"[\s~^:?*\[\\]", branch):
        raise ValueError("Branch must use ai/* or control-hub/* and contain no invalid Git ref characters.")
    repo = _request("GET", _repo_path())
    default = repo["default_branch"]
    base = _request("GET", _repo_path(f"/git/ref/heads/{quote(default, safe='/')}"))
    _request("POST", _repo_path("/git/refs"), json={
        "ref": f"refs/heads/{branch}",
        "sha": base["object"]["sha"],
    })
    return {"branch": branch, "base": default}


@mcp.tool()
def commit_repo_file(path: str, content: str, branch: str, message: str, current_file_sha: str = "") -> dict[str, str]:
    """Create/update a UTF-8 file on an ai/* or control-hub/* branch; never write to the default branch."""
    if not _branch_ok(branch):
        raise ValueError("Writes are restricted to ai/* and control-hub/* branches.")
    if path.startswith("/") or ".." in path.split("/") or "\x00" in path:
        raise ValueError("Unsafe repository path.")
    encoded = content.encode("utf-8")
    if len(encoded) > MAX_FILE_BYTES:
        raise ValueError("File exceeds the 500 KB write limit.")
    if not message.strip() or len(message) > 200:
        raise ValueError("Commit message must be 1–200 characters.")
    payload: dict[str, Any] = {
        "message": message,
        "content": base64.b64encode(encoded).decode("ascii"),
        "branch": branch,
    }
    if current_file_sha:
        payload["sha"] = current_file_sha
    result = _request("PUT", _repo_path(f"/contents/{quote(path, safe='/')}"), json=payload)
    return {"path": path, "commit_sha": result["commit"]["sha"], "branch": branch}


@mcp.tool()
def open_repo_pr(branch: str, title: str, body: str = "") -> dict[str, Any]:
    """Open a PR from an ai/* or control-hub/* branch to the repository default branch."""
    if not _branch_ok(branch):
        raise ValueError("PR head must use ai/* or control-hub/*.")
    repo = _request("GET", _repo_path())
    result = _request("POST", _repo_path("/pulls"), json={
        "title": title[:250],
        "head": branch,
        "base": repo["default_branch"],
        "body": body[:60_000],
        "maintainer_can_modify": True,
    })
    return {"number": result["number"], "url": result["html_url"], "state": result["state"]}


@mcp.tool()
def dispatch_ci(workflow_file: str = "ci.yml", branch: str = "") -> dict[str, str]:
    """Dispatch an existing GitHub Actions workflow on an allowed feature branch."""
    if not _branch_ok(branch):
        raise ValueError("CI dispatch is restricted to ai/* and control-hub/* branches.")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+\.ya?ml", workflow_file):
        raise ValueError("Provide a workflow filename such as ci.yml.")
    _request("POST", _repo_path(f"/actions/workflows/{quote(workflow_file)}/dispatches"),
             json={"ref": branch})
    return {"workflow": workflow_file, "branch": branch, "status": "dispatched; check Actions for completion"}


if __name__ == "__main__":
    mcp.run(transport="stdio")
