---
name: clinicaltrials-gov-api
description: Use this skill when working with the ClinicalTrials.gov Data API v2, including building official query syntax, calling `/api/v2/studies` or `/api/v2/studies/{NCT_ID}`, selecting field paths, paginating with `nextPageToken`, checking API/data version metadata, and producing structured trial summaries from API responses.
---

# ClinicalTrials.gov API

## Overview

Use this skill to make reliable, reproducible requests to the ClinicalTrials.gov v2 API and convert raw responses into concise trial summaries.

## Workflow

1. Confirm the task goal and output shape.
2. Choose the endpoint.
3. Build query/filter parameters using official syntax.
4. Add fields, sorting, and pagination controls.
5. Execute request and validate response metadata.
6. Summarize with explicit caveats for missing fields.

## Endpoint Choice

- Use `GET /api/v2/studies` to search/browse studies.
- Use `GET /api/v2/studies/{NCT_ID}` to retrieve one study record.
- Use `GET /api/v2/version` to report `apiVersion` and `dataTimestamp`.

## Query Construction Rules

- Prefer `query.*` parameters for search terms (`query.cond`, `query.term`, `query.locn`, etc.).
- Use `filter.*` parameters for post-search filtering (`filter.overallStatus`, date ranges, geo distance filters).
- Use `query.id` for explicit NCT IDs when the request gives exact identifiers.
- Use `query.expr` for advanced boolean/range expressions when simple query parameters are not enough.
- For complex `query.expr`, follow AREA/RANGE syntax from `references/query-syntax.md`.

## Response Shaping Rules

- Use `fields` to request only needed paths for payload reduction.
- Use `sort` only when ordering is required by the task.
- Use `pageSize` plus `pageToken` for pagination loops.
- Treat `nextPageToken` as the continuation signal.
- Use `countTotal=true` only when total counts are explicitly needed.

## Scripts

- Use `scripts/search_studies.py` for search calls with common query/filter args.
- Use `scripts/get_study.py` for single-study retrieval by NCT ID.
- Use `scripts/get_version.py` to report API/data freshness metadata.

## Minimal Command Patterns

```bash
# Search with condition keyword and selected fields
./scripts/search_studies.py --cond "lung cancer" --field "protocolSection.identificationModule.nctId" --field "protocolSection.identificationModule.briefTitle" --page-size 10 --pretty

# Retrieve one trial
./scripts/get_study.py NCT04280705 --pretty

# Check API/data freshness
./scripts/get_version.py --pretty
```

## Output Standards

- Include NCT ID, short title, status, and phase when present.
- State when a value is missing instead of inferring.
- For ranked/filtered outputs, state the exact parameters used.
- For time-sensitive answers, include the `dataTimestamp` from `/api/v2/version` when available.

## Resources

- Syntax reference: `references/query-syntax.md`
- Endpoint and field-path guide: `references/api-reference.md`
