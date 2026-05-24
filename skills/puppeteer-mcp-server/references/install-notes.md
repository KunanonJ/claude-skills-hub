# Puppeteer MCP Server Install Notes

## Source

- Repository: https://github.com/merajmehrabi/puppeteer-mcp-server
- npm package: `puppeteer-mcp-server`
- Installed npm version: `0.7.2`
- Verified source revision during install: `41d656953cba033d6d993ccca589be72c2e1db3f`

## Local Codex Integration

Codex uses `/Users/kunanonjarat/.codex/bin/puppeteer-mcp-server.sh`.

The wrapper:

- runs `npx -y puppeteer-mcp-server@0.7.2`,
- uses `/Users/kunanonjarat/.codex/mcp-runtime/puppeteer-mcp-server` as the working directory,
- keeps the upstream Winston `logs/` directory out of arbitrary project folders,
- sets `PUPPETEER_CACHE_DIR` to `/Users/kunanonjarat/.codex/cache/puppeteer-mcp-server`,
- does not require credentials.

## Upstream Behavior To Know

- Local NPX mode launches Puppeteer with `headless: false`.
- Local NPX mode passes browser flags that disable web security and site isolation.
- The server can connect to existing Chrome windows through a local remote-debugging port.
- The tool set includes navigation, screenshot, click, fill, select, hover, and JavaScript evaluation.

## Recommended Use

Use this MCP for Puppeteer-specific browser automation or active Chrome tab workflows. For ordinary local frontend testing, prefer the existing Browser, Chrome DevTools, or Playwright tools unless Puppeteer is explicitly needed.

## Active Chrome Tab Setup

Close existing Chrome instances before starting active-tab mode, then launch Chrome with:

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
```

Remote debugging should stay bound to the local machine and should be closed when no longer needed.
