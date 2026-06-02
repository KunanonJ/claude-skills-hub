# Workspace Memory Query Contract

## Transport

Driver invocation remains file-transport compatible with legacy backend adapters:

- request payload: `--payload-path`
- response payload: `--response-path`
- lane/action routing: `--lane`, `--action`

## Required CLI Inputs

- `--lane`: `serena | ruflo | cognee`
- `--action`: `read | write`
- `--repo-root`: workspace anchor used to resolve `.vibeskills/project.json`
- `--payload-path`
- `--response-path`
- `--project-key` (optional, required for Serena read/write)

`--store-path` and `--session-root` are accepted for compatibility but storage resolution is broker-owned.

## Read Request Shape

- Common:
  - `task`: retrieval query text
  - `top_k`: max records (optional)
  - `keywords`: optional query hints
- Lane-specific:
  - `serena`: decision query
  - `ruflo`: handoff card query
  - `cognee`: relation query

## Write Request Shape

- `serena`: `decisions[]`
- `ruflo`: `cards[]`, optional `run_id`, optional `task`
- `cognee`: `relations[]`, optional `task`

## Response Shape

- Compatibility fields:
  - `ok`, `status`, `lane`
  - `item_count`, `items`
  - `project_key`, `project_key_source`
  - `store_path`
- Workspace plane fields:
  - `driver_mode`
  - `capsule_count`, `capsules`
  - `suppressed_count`
  - `workspace_memory_plane`:
    - `workspace_id`
    - `workspace_root`
    - `workspace_sidecar_root`
    - `descriptor_path`
    - `plane_path`

## Noise Admission Statuses

- `backend_write`: all candidate writes admitted
- `backend_write_with_noise_suppressed`: partial admission
- `guarded_noise_suppressed`: all candidates filtered as noise
- `guarded_no_write`: no admissible input or missing Serena project key
