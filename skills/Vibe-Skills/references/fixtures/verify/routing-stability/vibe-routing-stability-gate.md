# VCO Routing Stability Gate

- Mode: `default`
- Generated: `2026-04-28T13:42:54`
- Gate Passed: `True`
- Stricter Rules Ready: `True`

## Metrics

- route_stability: `0.9444` (threshold `0.75`)
- top1_top2_gap: `0.246` (threshold `0.051`)
- fallback_rate: `0` (threshold `0.85`)
- misroute_rate: `0.1` (threshold `0.3`)

## Group Stability

- `ai-llm-research-embedding`: stability=`1` dominant=`ai-llm|embedding-strategies`
- `ai-llm-research-openai-docs`: stability=`1` dominant=`ai-llm|openai-docs`
- `aios-core-planning-pm`: stability=`1` dominant=`aios-core|aios-master`
- `aios-core-planning-po`: stability=`1` dominant=`aios-core|aios-master`
- `code-quality-review`: stability=`1` dominant=`code-quality|code-reviewer`
- `data-ml-research`: stability=`0.6667` dominant=`data-ml|scikit-learn`
- `docs-media-coding-tabular`: stability=`1` dominant=`docs-media|spreadsheet`
- `docs-media-coding-xlsx`: stability=`1` dominant=`docs-media|xlsx`
- `integration-devops-ci-debug`: stability=`1` dominant=`integration-devops|gh-fix-ci`
- `integration-devops-sentry-debug`: stability=`1` dominant=`integration-devops|sentry`
- `planning-no-orchestration-core`: stability=`0.6667` dominant=`scholarly-publishing-workflow|scholarly-publishing`
- `research-design-planning`: stability=`1` dominant=`research-design|designing-experiments`
