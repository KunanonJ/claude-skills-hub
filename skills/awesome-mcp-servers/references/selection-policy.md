# MCP Server Selection Policy

## Candidate Review Checklist

Before recommending or installing a server found in `awesome-mcp-servers`, verify:

- The server repo is the authoritative source for install instructions.
- The package name, binary, Docker image, or `uvx` command matches the repo docs.
- The server supports the target MCP host transport: stdio, Streamable HTTP, SSE, or bridge.
- Required credentials are identified and can be supplied without hardcoding secrets.
- Tool permissions are scoped to the user's use case.
- Startup can be verified with `--help`, an MCP inspector, or a safe handshake.
- Existing installed plugins or MCP servers do not already cover the same capability.

## Safety Defaults

- Do not install from catalog text alone. Always inspect the selected server repo.
- Do not install servers that require unknown paid APIs, wallet payments, browser session access, production cloud access, or database write access without explicit approval.
- For cloud and SaaS integrations, prefer read-only scopes first.
- For local filesystem, browser, shell, or IDE automation, prefer allowlists and user-visible working directories.
- For aggregators and meta-MCP servers, validate that tool discovery does not explode the context window or bypass security controls.

## Ranking Heuristics

Rank candidates by:

1. Official implementation marker, when present.
2. Active maintenance and clear installation docs.
3. Small, auditable permission surface.
4. Native support for the user's platform.
5. Existing local dependencies already available on the machine.
6. Simple verification path without production credentials.
7. Fit to the user's exact task over raw tool count.

## Output Format

When presenting options, include:

- Candidate name and repo URL.
- Why it fits the use case.
- Local/cloud scope and language/runtime.
- Required credentials or external services.
- Install risk tier.
- Verification command or smoke test.
- Recommendation: install now, inspect first, or skip.
