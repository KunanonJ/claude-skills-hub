---
description: Fetch stargazer locations, classify regions, and generate a region breakdown chart
argument-hint: <owner/repo>
---

Generate a region breakdown chart for: $ARGUMENTS

## Steps

### 1. Fetch stargazer data

Run the CLI to fetch all stargazers with locations (this caches the data):

```
npx gh-star-region <owner/repo> --no-open
```

This will paginate through all stargazers via the GitHub GraphQL API and cache the results.

### 2. Find unclassified locations

Run the unclassified locations script:

```
npx gh-star-unclassified <owner/repo> > /tmp/unclassified.csv
```

If all locations are already classified, skip to step 5.

### 3. Classify locations into regions

Split `/tmp/unclassified.csv` into batches of ~200 and spawn parallel subagents to classify each batch. Each subagent should:

- Read its batch file (e.g., `/tmp/locations_batch_0.csv`)
- Determine the region for each location
- Write output to `/tmp/locations_classified_0.csv` with columns: `location, count, region`

Classification rules:
- Use standard region names (e.g., "South Korea", "United States", "China")
- US cities/states -> "United States"
- Chinese characters (深圳, 北京, etc.) -> "China"
- Korean characters (서울, etc.) -> "South Korea"
- Ambiguous/joke locations ("Earth", "localhost", "Matrix") -> "Unknown"
- Keep the exact original location string

### 4. Update location map

Merge the new classified locations into `~/.gh-star-history/location_region_map.json`, adding any new mappings that don't already exist (skip "Unknown" entries).

### 5. Generate the chart

Run the CLI again to generate the chart with updated mappings:

```
npx gh-star-region <owner/repo>
```

This will open the chart in the browser automatically. Do NOT run a separate `open` command.
