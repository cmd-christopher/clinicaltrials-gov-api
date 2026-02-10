# Query Syntax Guide

Primary reference: <https://clinicaltrials.gov/api/gui/ref/syntax>

## Choose Query Mode

- Use simple `query.*` parameters for straightforward requests.
- Use `query.expr` when you need boolean logic, explicit field targeting, or ranges.

## Building `query.expr`

- Use boolean operators: `AND`, `OR`, `NOT`.
- Use field scoping with `AREA[...]` expressions.
- Use ranges with `RANGE[...]` expressions for dates/numeric filters.
- Quote multi-word phrases when exact phrasing matters.

## Practical Patterns

- Broad keyword search:
  - Prefer `query.term=<text>`
- Condition-focused search:
  - Prefer `query.cond=<condition text>`
- Exact trial IDs:
  - Prefer `query.id=<NCT IDs>`
- Complex expression:
  - Use `query.expr=<AREA/RANGE boolean expression>`

## Debugging Strategy

1. Start with one simple parameter.
2. Add one filter at a time.
3. Add `fields` only after verifying matches.
4. Add `sort` and pagination last.
5. If results are empty, remove expression terms incrementally to find the failing clause.

## Pagination Rules

- Use `pageSize` to control records per page.
- Use returned `nextPageToken` as the next request's `pageToken`.
- Stop when `nextPageToken` is absent.

## Reproducibility

- Save the full request URL used for final answers.
- Include API `dataTimestamp` from `/api/v2/version` for time-sensitive output.
