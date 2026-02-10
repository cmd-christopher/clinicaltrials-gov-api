# ClinicalTrials.gov v2 API Reference

## Official Sources

- API overview and interactive docs: <https://clinicaltrials.gov/data-api/api#refs>
- OpenAPI spec endpoint: <https://clinicaltrials.gov/api/oas/v2>
- API URL reference: <https://clinicaltrials.gov/api/gui/ref/api_urls>
- Query syntax reference: <https://clinicaltrials.gov/api/gui/ref/syntax>
- API field metadata: <https://clinicaltrials.gov/api/gui/ref/api_fields>
- About API and migration notes: <https://clinicaltrials.gov/data-api/about-api>
- Data status: <https://clinicaltrials.gov/data-api/about-api/data-status>

## Base URL

- `https://clinicaltrials.gov/api/v2`

## Core Endpoints

- `GET /studies`
  - Search and list studies.
- `GET /studies/{NCT_ID}`
  - Retrieve a single study by NCT ID.
- `GET /version`
  - Return API/data metadata such as `apiVersion` and `dataTimestamp`.

## Common `/studies` Query Parameters

- Response shape: `format`, `markupFormat`, `fields`
- Query terms: `query.term`, `query.cond`, `query.intr`, `query.titles`, `query.outc`, `query.spons`, `query.lead`, `query.patient`, `query.id`, `query.locn`
- Query expression mode: `query.expr`
- Filters: `filter.overallStatus`, `filter.geo`, `filter.ids`, `filter.advanced`, `filter.synonyms`
- Ordering/pagination: `sort`, `pageSize`, `pageToken`, `countTotal`

If parameter behavior differs across API versions, trust the live API GUI and OpenAPI spec.

## Response Structure Notes

- Search responses contain `studies` (array).
- Pagination continuation appears as `nextPageToken`.
- Top-level metadata may include `totalCount` when `countTotal=true`.
- Individual study records are organized by modules (for example `protocolSection`, `resultsSection`, `derivedSection`, `annotationsSection`, `documentSection`).

## Field Path Usage

`fields` accepts field paths (dot notation). Example field paths:

- `protocolSection.identificationModule.nctId`
- `protocolSection.identificationModule.briefTitle`
- `protocolSection.statusModule.overallStatus`
- `protocolSection.designModule.phases`

Use field filtering aggressively for smaller payloads and faster responses.

## Freshness / Time-Sensitive Reporting

- Call `GET /version` and include `dataTimestamp` when reporting recency.
- Data refresh and ingest status are documented on the data-status page.

## Migration Highlights (Legacy to v2)

- API v2 replaces the classic API and supports JSON-first usage with OpenAPI documentation.
- Enumeration/value normalization and richer field typing are part of the modernization changes.
- Always verify legacy parameter names before reusing old scripts.
