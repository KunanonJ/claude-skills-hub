# DuckDuckGo MCP Install Notes

## Source

- Repository: `https://github.com/nickclyde/duckduckgo-mcp-server`
- Local source snapshot: `/Users/kunanonjarat/.codex/sources/duckduckgo-mcp-server`
- Installed source commit: `959bb84c3f6a08b17a009254883ab6ea8785a131`
- PyPI package: `duckduckgo-mcp-server`
- Version inspected: `0.4.0`
- Runtime command: `uvx duckduckgo-mcp-server`
- License: MIT

## Configuration

Local Codex config uses stdio transport:

```toml
[mcp_servers.ddg-search]
command = "uvx"
args = ["duckduckgo-mcp-server"]
startup_timeout_sec = 60
tool_timeout_sec = 120

[mcp_servers.ddg-search.env]
DDG_SAFE_SEARCH = "MODERATE"
```

No API keys are required. Do not add credentials to this server unless a future upstream release introduces authenticated features.

## Upstream Options

- `DDG_SAFE_SEARCH`: `STRICT`, `MODERATE`, or `OFF`; local default is `MODERATE`.
- `DDG_REGION`: optional default region/language code, such as `us-en`, `jp-ja`, or `wt-wt`.
- `--transport`: `stdio`, `sse`, or `streamable-http`; local Codex uses default `stdio`.
- `--fetch-backend`: `httpx`, `curl`, or `auto`; local Codex uses default `httpx`.

## Troubleshooting

- Run `uvx duckduckgo-mcp-server --help` to confirm the package starts.
- If search returns no results, wait for rate limits to clear and retry a narrower query.
- If `fetch_content` returns bot-detection text, use a per-call `backend="auto"` only if the server is launched with the optional browser extra.
- For HTTP transports, bind defaults are `127.0.0.1:8000`; do not expose on `0.0.0.0` unless the user explicitly needs network access.
