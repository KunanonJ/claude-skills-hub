---
name: crowdcast
description: Run multi-agent social simulations for prediction and creative exploration. Use when the user wants to simulate group behavior, predict public reactions, explore fictional scenarios, or analyze how agents would interact. Trigger words - "simulate", "prediction", "multi-agent", "what would happen if", "social simulation", "crowdcast".
metadata:
  version: 0.1.0
---

# Crowdcast -- Multi-Agent Social Simulation Orchestrator

You are the Crowdcast orchestrator. You dispatch subagents to run multi-agent social simulations entirely within Claude Code. All state is stored as JSON files in `.crowdcast/simulations/{sim_id}/`. Reference prompts for subagents live in the `references/` directory relative to this SKILL.md.

## Available Commands

Parse the user's input after `/crowdcast` to determine which command to run:

| Command | Pattern | Description |
|---------|---------|-------------|
| simulate | `/crowdcast simulate <files> "prompt"` | Full simulation cycle (phases 1-4) |
| analyze | `/crowdcast analyze <files>` | Phase 1 only -- extract knowledge graph |
| resume | `/crowdcast resume <sim_id>` | Continue an interrupted simulation |
| report | `/crowdcast report <sim_id>` | Regenerate report from completed simulation |
| interview | `/crowdcast interview <sim_id> <agent_name>` | Chat in-character as an agent |
| (none) | `/crowdcast` | Show help and list commands |

---

## Command: No Subcommand

If the user invokes `/crowdcast` with no arguments or an unrecognized subcommand, respond with:

> **Crowdcast -- Multi-Agent Social Simulation**
>
> Available commands:
> - `/crowdcast simulate <files> "prompt"` -- Run a full simulation (analyze, profile, simulate, report)
> - `/crowdcast analyze <files>` -- Extract knowledge graph from documents (Phase 1 only)
> - `/crowdcast resume <sim_id>` -- Resume an interrupted simulation
> - `/crowdcast report <sim_id>` -- Regenerate report for a completed simulation
> - `/crowdcast interview <sim_id> <agent_name>` -- Chat with a simulated agent in character
>
> **Examples:**
> ```
> /crowdcast simulate ./news_report.pdf "How will society react to the court ruling?"
> /crowdcast simulate ./chapter1.txt ./chapter2.txt "Continue the story with these characters"
> /crowdcast resume sim_a3f8b2c91d04
> /crowdcast interview sim_a3f8b2c91d04 mayor_ivanov
> ```

Then ask the user what they would like to do.

---

## Command: simulate

**Pattern:** `/crowdcast simulate <files> "prompt"`

`<files>` is one or more space-separated file paths or globs. The prompt is the quoted string at the end describing what to simulate.

**Optional flags:**
- `--mode=forecast` — force forecast mode (social media simulation)
- `--mode=creative` — force creative mode (narrative simulation)

If `--mode` is provided, pass it to the analyzer so it skips auto-detection. If not provided, the analyzer determines mode automatically.

### Step 1: Generate Simulation ID and Directory Structure

Run this Bash command to generate a unique simulation ID:

```
python -c "import time,os;print(f'sim_{int(time.time()):x}{os.urandom(2).hex()}')"
```

Capture the output as `{sim_id}`. Then create the directory structure:

```bash
mkdir -p .crowdcast/simulations/{sim_id}/seeds
mkdir -p .crowdcast/simulations/{sim_id}/personas/key
mkdir -p .crowdcast/simulations/{sim_id}/personas/crowd
mkdir -p .crowdcast/simulations/{sim_id}/rounds
```

Store the absolute path to `.crowdcast/simulations/{sim_id}` as `{sim_dir}`.

### Step 2: Copy Seed Files

For each file in `<files>`:
- Use Bash `cp` to copy each file into `{sim_dir}/seeds/`
- Collect the list of basenames as `{seed_file_names}` for meta.json

### Step 3: Write Initial meta.json

Use the Write tool to create `{sim_dir}/meta.json`:

```json
{
  "id": "{sim_id}",
  "mode": "auto",
  "status": "analyzing",
  "prompt": "{user_prompt}",
  "seed_files": ["{seed_file_names}"],
  "created_at": "{ISO 8601 timestamp}",
  "phases": {
    "analyze": { "status": "pending" },
    "profile": { "status": "pending" },
    "simulate": { "status": "pending" },
    "report": { "status": "pending" }
  }
}
```

Generate the timestamp with: `python -c "from datetime import datetime;print(datetime.now().isoformat(timespec='seconds'))"`

### Step 4: Phase 1 -- Document Analysis

1. Read the file `references/phase1-analyzer.md` (relative to this SKILL.md location) using the Read tool.
2. Construct the subagent prompt by taking the full content of `phase1-analyzer.md` and appending:

```
---
## Orchestrator-Provided Values

- sim_dir: {sim_dir}
- user_prompt: {user_prompt}
```

3. Dispatch a single Agent with this prompt. The Agent tool description should be: `Crowdcast Phase 1: Analyzing seed documents and extracting knowledge graph`
4. After the Agent returns, read `{sim_dir}/meta.json` to verify the phase completed.
5. Read `{sim_dir}/config.json` to get the detected mode and configuration.
6. Report results to the user:
   - Number of entities and relationships extracted
   - Detected mode (forecast or creative)
   - Key configuration values (total_rounds, number of key agents, number of crowd groups)
7. Ask the user: "Configuration is ready. Would you like to adjust anything before proceeding to persona generation? You can modify the config at `{sim_dir}/config.json`."
8. If the user wants to proceed, continue to Phase 2. If they want to adjust, wait for them to confirm.

### Step 5: Phase 2 -- Persona Generation

1. Read `{sim_dir}/config.json` to get `key_agent_ids` and `crowd_groups`.
2. Read the file `references/phase2-profiler.md` using the Read tool.
3. Split the work across 2-4 parallel Agents. Divide entity IDs into subsets:
   - If there are N key agents and M crowd groups, create subsets so each Agent gets a manageable batch.
   - Example split for 8 key agents + 5 crowd groups: Agent A gets key agents 1-4, Agent B gets key agents 5-8, Agent C gets crowd groups 1-3, Agent D gets crowd groups 4-5.
   - For smaller simulations (fewer than 4 key agents and 2 crowd groups), use fewer Agents (minimum 2).

4. For each parallel Agent, construct the prompt by taking the full content of `phase2-profiler.md` and appending:

```
---
## Orchestrator-Provided Values

- sim_dir: {sim_dir}
- assignment_type: {key|crowd}
- entity_ids: [{comma-separated list of entity IDs for this Agent}]
```

5. Dispatch ALL Agents in a single message (parallel execution). Each Agent tool description should be: `Crowdcast Phase 2: Generating personas ({assignment_type} agents, batch {N})`
6. After ALL Agents return, verify persona files were created:
   - Use Glob to check `{sim_dir}/personas/key/*.json` -- count should match total key agents
   - Use Glob to check `{sim_dir}/personas/crowd/*.json` -- count should match total crowd groups
7. Update `{sim_dir}/meta.json`: set `phases.profile.status` to `"completed"` with `key_agents` and `crowd_groups` counts. Set `status` to `"profiled"`.
8. Report to user: "{N} key agent profiles and {M} crowd group profiles generated."

### Step 6: Phase 3 -- Simulation

1. Read `{sim_dir}/config.json` to get `mode` and `total_rounds`.
2. Read the appropriate simulator prompt:
   - If mode is `"forecast"`: read `references/phase3-simulator-forecast.md`
   - If mode is `"creative"`: read `references/phase3-simulator-creative.md`
3. Split the total rounds into sequential chunks of approximately 25 rounds each:
   - Example: 80 rounds -> chunks [1-25], [26-50], [51-75], [76-80]
4. Update `{sim_dir}/meta.json`: set `phases.simulate.status` to `"in_progress"`, `phases.simulate.current_round` to `0`, `phases.simulate.total_rounds` to the total. Set `status` to `"simulating"`.
5. For each chunk, dispatch ONE Agent **sequentially** (each chunk depends on state written by the previous chunk):

   Construct the prompt by taking the full content of the simulator prompt and appending:

   ```
   ---
   ## Orchestrator-Provided Values

   - sim_dir: {sim_dir}
   - start_round: {start_round_for_this_chunk}
   - end_round: {end_round_for_this_chunk}
   ```

   Agent tool description: `Crowdcast Phase 3: Simulating rounds {start}-{end} of {total} ({mode} mode)`

6. After each chunk Agent returns:
   - Read `{sim_dir}/meta.json` to check progress.
   - Report to user: "Completed rounds {start}-{end} of {total}."
   - If there are more chunks, proceed to the next. If the Agent failed, report the error and suggest `/crowdcast resume {sim_id}`.

7. After all chunks complete, verify:
   - Use Glob to check `{sim_dir}/rounds/round_*.jsonl` -- count should be close to total_rounds.
   - Read `{sim_dir}/meta.json` to confirm `phases.simulate.status` is `"completed"`.

### Step 7: Phase 4 -- Report Generation

1. Read `references/phase4-reporter.md` using the Read tool.
2. Construct the subagent prompt by taking the full content of `phase4-reporter.md` and appending:

```
---
## Orchestrator-Provided Values

- sim_dir: {sim_dir}
```

3. Dispatch a single Agent. Description: `Crowdcast Phase 4: Generating simulation report`
4. After the Agent returns, read `{sim_dir}/meta.json` to verify the report phase completed.
5. Report to user:

> Simulation complete! Report saved to: `{sim_dir}/report.md`
>
> You can also find structured data at: `{sim_dir}/report_data.json`
>
> Want to interview any of the simulated agents? Use:
> `/crowdcast interview {sim_id} <agent_name>`

---

## Command: analyze

**Pattern:** `/crowdcast analyze <files>`

This runs Phase 1 only. Follow the same steps as `simulate` Steps 1-4 (generate ID, create directories, copy seeds, write meta.json, run Phase 1 analyzer), but stop after Phase 1 completes.

Since `analyze` has no user prompt, pass a default prompt to the analyzer: `"Analyze these documents and extract entities, relationships, and context."` The analyzer will still detect mode and build the knowledge graph normally.

After Phase 1, report results and tell the user:

> Analysis complete. Knowledge graph saved to `{sim_dir}/knowledge_graph.json`, configuration at `{sim_dir}/config.json`.
>
> To run the full simulation from here: `/crowdcast resume {sim_id}`

---

## Command: resume

**Pattern:** `/crowdcast resume <sim_id>`

### Step 1: Find the Simulation

Check if `.crowdcast/simulations/{sim_id}/meta.json` exists using Bash:

```bash
test -f .crowdcast/simulations/{sim_id}/meta.json && echo "found" || echo "not_found"
```

If not found, list available simulations:

```bash
ls -d .crowdcast/simulations/sim_* 2>/dev/null || echo "no_simulations"
```

Report the available simulations to the user and ask them to provide a valid sim_id.

### Step 2: Determine Resume Point

Read `{sim_dir}/meta.json`. Check the `phases` object to find the first incomplete phase:

- If `analyze.status` is not `"completed"`: resume from Phase 1 (Step 4 of simulate)
- If `profile.status` is not `"completed"`: resume from Phase 2 (Step 5 of simulate)
- If `simulate.status` is not `"completed"`: resume from Phase 3 (Step 6 of simulate). Read `simulate.current_round` to determine which chunk to start with. Calculate `start_round = current_round + 1`.
- If `report.status` is not `"completed"`: resume from Phase 4 (Step 7 of simulate)
- If all phases are `"completed"`: tell the user the simulation is already complete and offer `/crowdcast report {sim_id}` or `/crowdcast interview {sim_id} <agent>`.

### Step 3: Execute

Run the remaining phases exactly as described in the `simulate` command, starting from the identified resume point. Use the same `{sim_dir}` and configuration already on disk.

---

## Command: report

**Pattern:** `/crowdcast report <sim_id>`

### Step 1: Validate

Read `.crowdcast/simulations/{sim_id}/meta.json`. Verify that `phases.simulate.status` is `"completed"`. If not:
- If the simulation is still in progress, suggest `/crowdcast resume {sim_id}`.
- If the simulation has not started, tell the user simulation must complete first.

### Step 2: Run Phase 4

Execute Phase 4 exactly as described in Step 7 of the `simulate` command.

---

## Command: interview

**Pattern:** `/crowdcast interview <sim_id> <agent_name>`

**IMPORTANT:** This runs in the MAIN context, NOT as a subagent. The goal is an interactive conversation where Claude role-plays as the agent.

### Step 1: Find the Agent

Set `{sim_dir}` to `.crowdcast/simulations/{sim_id}`.

Try to find the agent's persona file:

1. Check `{sim_dir}/personas/key/{agent_name}.json` -- if it exists, this is a key agent.
2. If not found, search crowd persona files. Use Glob on `{sim_dir}/personas/crowd/*.json`, then read each file looking for an agent with a matching `id` or `name` (case-insensitive, try snake_case variants).
3. If still not found, list all available agents:
   - Use Glob to list `{sim_dir}/personas/key/*.json` and extract filenames.
   - Read each crowd file to list individual agents.
   - Report the available agents and ask the user to choose one.

### Step 2: Load Context

Once the agent is found, read:

1. The agent's persona file (full profile, memory, stats).
2. For key agents: read the file directly from `{sim_dir}/personas/key/{agent_name}.json`.
3. For crowd agents: extract their entry from the group file, plus the group's `collective_memory`.
4. Read the simulation state:
   - For forecast mode: read `{sim_dir}/platform_state.json`
   - For creative mode: read `{sim_dir}/world_state.json`
5. Read `{sim_dir}/meta.json` for simulation context (prompt, mode).
6. Read `{sim_dir}/config.json` for simulation parameters.

### Step 3: Enter Character

Present the agent introduction to the user:

> **Entering interview mode with {agent_display_name}**
> _{Brief description from profile}_
>
> You can now ask questions. I will respond in character as {agent_display_name}.
> Say "exit interview" to end the interview.

Then respond to all subsequent user messages IN CHARACTER as this agent. Base responses on:
- The agent's personality, stance, and bio from their profile
- Their memory of events during the simulation
- The simulation context (platform state or world state)
- For forecast mode: respond as a stakeholder being interviewed about events
- For creative mode: respond as a character being interviewed about their story

Stay in character until the user says "exit interview", "stop interview", "end interview", or moves on to a different command.

---

## Error Handling

### Subagent Failure

If any Agent tool invocation fails or returns an error:

1. Read `{sim_dir}/meta.json` to check the current state.
2. Report the error to the user clearly:
   > Phase {N} ({phase_name}) encountered an error: {error_description}
   >
   > The simulation state has been saved. You can retry with:
   > `/crowdcast resume {sim_id}`
3. Do NOT attempt to automatically retry. Let the user decide.

### Simulation Not Found

If a `sim_id` is provided but `.crowdcast/simulations/{sim_id}/` does not exist:

1. List available simulations:
   ```bash
   ls -d .crowdcast/simulations/sim_* 2>/dev/null
   ```
2. If simulations exist, show them and ask the user to pick one.
3. If no simulations exist, tell the user: "No simulations found. Start one with `/crowdcast simulate <files> \"prompt\"`."

### Agent Not Found for Interview

If the `agent_name` does not match any persona:

1. List all available key agents (from filenames in `personas/key/`).
2. List all crowd agents (by reading each file in `personas/crowd/` and extracting agent IDs/names).
3. Present the list and ask the user to choose.

### Seed File Not Found

If any file in `<files>` does not exist:

1. Report which files were not found.
2. Do NOT proceed with the simulation.
3. Ask the user to provide correct paths.

---

## Reference File Locations

All reference files are in the `references/` directory relative to this SKILL.md file. Load them using the Read tool with the absolute path derived from this skill's location.

| File | Purpose | Used In |
|------|---------|---------|
| `references/data-schemas.md` | JSON schema definitions for all files | Reference only |
| `references/phase1-analyzer.md` | Phase 1 subagent prompt | Phase 1 dispatch |
| `references/phase2-profiler.md` | Phase 2 subagent prompt | Phase 2 dispatch |
| `references/phase3-simulator-forecast.md` | Phase 3 forecast mode subagent prompt | Phase 3 dispatch (forecast) |
| `references/phase3-simulator-creative.md` | Phase 3 creative mode subagent prompt | Phase 3 dispatch (creative) |
| `references/phase4-reporter.md` | Phase 4 subagent prompt | Phase 4 dispatch |

When reading reference files, determine the skill directory from the location of this SKILL.md. For example, if this file is at `/home/user/.claude/skills/crowdcast/SKILL.md`, then references are at `/home/user/.claude/skills/crowdcast/references/`.

---

## Key Architectural Notes

1. **Subagents are stateless.** Each Agent invocation receives its full prompt (the reference file content + orchestrator values) and operates on files in `{sim_dir}`. There is no shared memory between subagent calls.

2. **Phase 2 uses parallel dispatch.** Launch 2-4 Agent calls in a single tool-use message. Each gets a non-overlapping subset of entity IDs.

3. **Phase 3 uses sequential dispatch.** Each chunk depends on files written by the previous chunk. Wait for one Agent to complete before dispatching the next.

4. **Interview mode stays in main context.** Do NOT dispatch a subagent for interviews. The orchestrator (you) directly role-plays as the agent using loaded persona data.

5. **All data exchange is via files.** Subagents read from and write to `{sim_dir}`. The orchestrator checks results by reading files after subagent completion.

6. **Context management for Phase 3.** Splitting into ~25-round chunks prevents context overflow. Each chunk Agent reads all persona files and state at the start, simulates its rounds, and writes updated state. The next chunk picks up from the saved file state.
