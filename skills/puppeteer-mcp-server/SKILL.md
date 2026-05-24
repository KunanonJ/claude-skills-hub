---
name: puppeteer-mcp-server
description: Use merajmehrabi/puppeteer-mcp-server from Codex for Puppeteer browser automation, screenshots, form interactions, JavaScript evaluation, and optional connection to existing Chrome tabs. Trigger when the user asks for puppeteer-mcp, Puppeteer MCP Server, browser automation through Puppeteer, active Chrome tab MCP control, or troubleshooting the local puppeteer-mcp install.
---

# Puppeteer MCP Server

## Core Rule

Use `puppeteer-mcp` only for browser automation that specifically benefits from Puppeteer or from connecting to an existing Chrome instance. Prefer the built-in Browser, Chrome DevTools, or Playwright MCP tools when they already cover the task with less risk or better local integration.

The Codex MCP server is configured as:

```toml
[mcp_servers.puppeteer-mcp]
command = "/Users/kunanonjarat/.codex/bin/puppeteer-mcp-server.sh"
startup_timeout_sec = 90
tool_timeout_sec = 300
```

The wrapper runs `npx -y puppeteer-mcp-server@0.7.2`, stores runtime logs under `$HOME/.codex/mcp-runtime/puppeteer-mcp-server/logs`, and stores Puppeteer browser downloads under `$HOME/.codex/cache/puppeteer-mcp-server`.

## Safety Policy

1. Treat browser automation as stateful and user-visible. Do not submit forms, send messages, make purchases, change settings, or perform account actions without explicit approval.
2. Treat `puppeteer_evaluate` as high risk on authenticated or sensitive pages because it executes JavaScript in page context.
3. Do not connect to an existing Chrome tab unless the user explicitly asks for active-tab mode or provides the target page context.
4. Remote debugging ports must remain local only. Never expose Chrome `--remote-debugging-port` to public networks.
5. Do not use this MCP to bypass paywalls, access controls, bot protections, or site terms.
6. Redact secrets from screenshots, console logs, and page output before summarizing results.

## Tool Surface

- `puppeteer_connect_active_tab`: connect to an existing Chrome instance with remote debugging enabled.
- `puppeteer_navigate`: navigate to a URL.
- `puppeteer_screenshot`: capture the page or a selected element.
- `puppeteer_click`: click an element.
- `puppeteer_fill`: fill an input.
- `puppeteer_select`: select an option.
- `puppeteer_hover`: hover an element.
- `puppeteer_evaluate`: execute JavaScript in the browser console.

## Active Tab Mode

Only use active-tab mode after explicit user intent. The upstream README starts Chrome like this on macOS:

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
```

Then connect with:

```json
{
  "debugPort": 9222
}
```

Use a unique local debugging port if another tool is already using `9222`.

## Troubleshooting

1. Confirm the wrapper starts with `/Users/kunanonjarat/.codex/bin/puppeteer-mcp-server.sh`.
2. Check local MCP registration with `codex mcp list`.
3. If startup is slow, the first run may be downloading Puppeteer's browser build into `$HOME/.codex/cache/puppeteer-mcp-server`.
4. If logs are needed, inspect `$HOME/.codex/mcp-runtime/puppeteer-mcp-server/logs`.
5. If local mode opens an unwanted visible browser, stop the MCP server and use Browser, Chrome DevTools, or Playwright instead.

## References

- Read `references/install-notes.md` before changing the local config or troubleshooting startup.
