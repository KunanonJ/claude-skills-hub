---
name: Composio Connect
description: Connect and execute actions over 1000+ apps using Composio
tags: [composio, tool-router, agents, mcp, tools, api, automation]
---

## When to use
Use this skill when:
- Authenticating and executing actions in external applications like (Slack, GitHub, Gmail, etc.)
- Making API requests to external applications
- Fetching data from external applications
- Making changes in external applications
- Analyzing data from external applications
- Assisting users in answering questions about their data

## Prerequisites
Make sure the below instructions are followed once. This is an optional requirement if all these are already followed.

### Installing the Composio CLI
1. Make sure Composio CLI is installed, run it once or when you encounter an error saying command doesn't exist
```bash
curl -fsSL https://composio.dev/install | bash
```

2. Verify the installation worked
```bash
composio --version
```
If it still says the command not found, you need to source the shell again. `source ~/.zshrc` for zsh, use relevant commands for other shells as well.

### Authenticating the user to Composio
1. Log the user in to Composio platform, this will return a URL which the user needs to authenticate.
```bash
composio login
```
2. Once the login is completed verify if the account is active.
```bash
composio whoami
```
> **Important**: This will display project_id, user_id, user_api_key etc. DO NOT use this to hardcode anything if you are writing code. 
> Use the above only as a reference to verify if the user is logged in.

## Using the Composio CLI to connect to 1000+ apps easily
Composio CLI allows users to authenticate and execute actions across 1000+ apps easily and securely.
It is very important to follow the below steps to achieve the best results.

### Step 1: Search for the specific tools
Given a usecase you have with connecting to external apps, and executing actions. Execute the `composio tools search` command to retrieve specific tools for the given use-case.

E.g., for sending emails
```bash
composio tools search "send emails"
```
E.g., for creating a Google Sheet
```bash
composio tools search "Create a new sheet in google sheet"
```

### Step 2: Execute the tool with appropriate data
E.g., once you have the tool information, you will know the input parameters required for executing the tool from the above command. Use the below `execute` command to run this tool.

> **Important** DO NOT make up the tool slugs, only use the tools returned by you from the `composio tools search` command.

```bash
composio tools execute "GMAIL_SEND_EMAIL" -d '{ "to": "hello@composio.dev", "body": "Hey, this is an email." }'
```

### Step 3: Authenticating the users to apps
If the above command fails stating no connected accounts, or the search returns the connection status as not connected, only then connect the user's account using the following command.


```bash
composio connected-accounts link "github"
```

> **Important** If you are unsure about the app name, use the `composio toolkits info 'gmail'`, or `composio tools info 'GMAIL_SEND_EMAIL'` to find the tool information and its toolkit information. DO NOT make up app names.

## Best practices

1. For reading json response from the CLI, pipe it to `jq`
2. Control the output at source, if you are fetching large amounts of data limit the required data being outputted using the tool's filters if it supports them.
3. If you are analysing data, after understanding the schema, offload the work to inline bash scripts or python scripts
4. If you are executing tools/actions which are independent, always do it in parallel using `&` and `wait`
5. Do not output large amount of data into the terminal, filter search and summarize with the right tools
  - Quick text filtering: `grep -E`, `rg` (ripgrep), `awk`, `sed`
  - Summarize instead of full dumps: `sort | uniq -c | sort -nr`, `wc -l`, `head`, `tail`
  - For huge files, use purpose-built viewers: `less`, `lnav` (logs), `tail -f` for streaming logs.
6. Do not create unnecessary cache files in the user's system, always use ephemeral files only when required, or create files only when the user explicitly asks.
7. Be mindful of rate limits and pagination (APIs/CLIs)
  - Parallelize carefully (`xargs -P`, `parallel`) only when you’re sure the backend can handle it.


## Important Notice
- Composio CLI contains a lot of other commands for developers. Do not use any other commands unless you are building apps.
- Only use this skill and Composio CLI for adhering to user requests regarding external apps.
- For an extensive guide on building apps and skills, refer to the documentation `https://docs.composio.dev`

