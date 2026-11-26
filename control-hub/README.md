# Vedra AI Development Control Hub

A repository-local control plane for AI coding agents. It gives MCP-capable clients a consistent, narrowly scoped GitHub toolset and provides a network-isolated Docker test runner.

## What is included

- `server.py`: MCP stdio server with GitHub repository, branch, file-commit, pull-request, and workflow-dispatch tools.
- `mcp-config.example.json`: client configuration example for MCP-compatible assistants.
- `Dockerfile` and `compose.yaml`: isolated development/test container. No Docker socket, host home directory, or production credentials are mounted.
- `.env.example`: names of required local configuration variables; never put real values in this file.
- `../.github/workflows/ci.yml`: pull-request checks for backend syntax and frontend build when the relevant project files exist.

## Setup (one time)

1. Create a fine-grained GitHub token restricted to **this repository only**. Grant:
   - Contents: Read and write
   - Pull requests: Read and write
   - Actions: Read and write (only needed to dispatch/check workflows)
   - Metadata: Read
   Do not grant Administration, Secrets, Workflows, or organization-wide access unless a future, explicitly reviewed integration needs it.
2. Save the token in your local environment as `GITHUB_TOKEN`; set `GITHUB_REPOSITORY=rahulrankesh/ai-portfolio`.
3. Install Python 3.11+ and run:
   ```bash
   cd control-hub
   python -m venv .venv
   . .venv/bin/activate
   pip install -r requirements.txt
   ```
4. Copy `mcp-config.example.json` into the MCP client's configuration and replace the command path with the absolute path to this repository's `control-hub/server.py`. Pass the token through the client's environment manager, not the JSON file.
5. Restart the MCP client. It should expose the Vedra GitHub tools.

## MCP tools

- `repo_overview`: repository metadata and default branch.
- `read_repo_file`: read a text file from a branch.
- `create_feature_branch`: branch from the default branch; only `ai/*` and `control-hub/*` names accepted.
- `commit_repo_file`: create/update a text file on an allowed feature branch.
- `open_repo_pr`: open a PR targeting the default branch.
- `dispatch_ci`: dispatch a configured GitHub Actions workflow and return the run URL when available.

This is a GitHub adapter, not a magic universal login. Claude, Cursor, VS Code agents, and other MCP-capable clients can connect if they support local stdio MCP. Each client must be configured separately. Other accounts (Vercel, cloud, databases, AI model providers) need their own provider OAuth/API authorization and least-privilege adapters; no credentials are fabricated or shared across vendors.

## Isolated test workspace

```bash
docker compose run --rm vedra-dev python -m compileall -q backend
```

The container has no network and only the repository working directory mounted. Add test commands to the allowlist in `server.py` only after reviewing their safety. For full frontend builds, dependencies must be prebuilt/cached in a separate controlled image or a temporary network-enabled build stage; runtime test containers remain network-isolated.

## Autonomy policy

Agents can branch, edit, test, commit, open PRs, and dispatch CI. Configure Vercel/other hosting separately before enabling deployments. Production deployments should use provider-side protected environments, scoped service identities, audit logs, and rollback support. Repository administration, secret changes, destructive operations, and production promotion remain owner-controlled.

## Operational limitations

- This server is intended for a trusted local machine. Do not expose stdio via an unauthenticated network bridge.
- The GitHub token is read from the process environment and is never returned by a tool.
- The MCP server commits files through GitHub's Contents API; local full-repository editing is done by the coding client in its own checkout.
- No checks have been run against external hosting or cloud accounts until those providers are connected.
