#!/usr/bin/env python3
"""Search ClinicalTrials.gov studies via API v2."""

import argparse
import json
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

DEFAULT_BASE_URL = "https://clinicaltrials.gov/api/v2/studies"
USER_AGENT = "clinicaltrials-gov-api-skill/1.0"


def parse_key_value(items):
    params = {}
    for item in items or []:
        if "=" not in item:
            raise ValueError(f"Invalid --param '{item}'. Use KEY=VALUE.")
        key, value = item.split("=", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"Invalid --param '{item}'. Empty key.")
        params[key] = value
    return params


def build_params(args):
    params = {
        "format": args.format,
        "pageSize": str(args.page_size),
    }

    if args.expr:
        params["query.expr"] = args.expr
    if args.term:
        params["query.term"] = args.term
    if args.cond:
        params["query.cond"] = args.cond
    if args.intr:
        params["query.intr"] = args.intr
    if args.titles:
        params["query.titles"] = args.titles
    if args.outc:
        params["query.outc"] = args.outc
    if args.spons:
        params["query.spons"] = args.spons
    if args.lead:
        params["query.lead"] = args.lead
    if args.patient:
        params["query.patient"] = args.patient
    if args.query_id:
        params["query.id"] = ",".join(args.query_id)
    if args.locn:
        params["query.locn"] = args.locn

    if args.overall_status:
        params["filter.overallStatus"] = ",".join(args.overall_status)

    if args.fields:
        params["fields"] = ",".join(args.fields)
    if args.sort:
        params["sort"] = args.sort
    if args.page_token:
        params["pageToken"] = args.page_token
    if args.count_total:
        params["countTotal"] = "true"

    params.update(parse_key_value(args.param))
    return params


def fetch(url):
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=30) as response:
        return response.read(), response.headers.get("Content-Type", "")


def write_output(body, output_path):
    if output_path:
        with open(output_path, "wb") as handle:
            handle.write(body)
    else:
        sys.stdout.buffer.write(body)


def main():
    parser = argparse.ArgumentParser(description="Search ClinicalTrials.gov studies")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--format", choices=["json", "csv"], default="json")
    parser.add_argument("--expr", help="Advanced query expression for query.expr")
    parser.add_argument("--term", help="query.term")
    parser.add_argument("--cond", help="query.cond")
    parser.add_argument("--intr", help="query.intr")
    parser.add_argument("--titles", help="query.titles")
    parser.add_argument("--outc", help="query.outc")
    parser.add_argument("--spons", help="query.spons")
    parser.add_argument("--lead", help="query.lead")
    parser.add_argument("--patient", help="query.patient")
    parser.add_argument("--query-id", action="append", help="query.id (repeatable)")
    parser.add_argument("--locn", help="query.locn")
    parser.add_argument("--overall-status", action="append", help="filter.overallStatus (repeatable)")
    parser.add_argument("--field", dest="fields", action="append", help="fields (repeatable field path)")
    parser.add_argument("--sort", help="sort expression")
    parser.add_argument("--page-size", type=int, default=20)
    parser.add_argument("--page-token", help="pageToken from prior response")
    parser.add_argument("--count-total", action="store_true", help="Set countTotal=true")
    parser.add_argument("--param", action="append", help="Additional raw parameter KEY=VALUE")
    parser.add_argument("--raw-url", action="store_true", help="Print the final URL to stderr")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    parser.add_argument("--output", help="Write output bytes to file")
    args = parser.parse_args()

    if args.page_size < 1:
        print("--page-size must be >= 1", file=sys.stderr)
        return 2

    try:
        params = build_params(args)
        url = f"{args.base_url}?{urlencode(params)}"

        if args.raw_url:
            print(url, file=sys.stderr)

        body, content_type = fetch(url)

        if args.format == "json" and "json" in content_type.lower() and args.pretty:
            parsed = json.loads(body.decode("utf-8"))
            pretty = (json.dumps(parsed, indent=2, ensure_ascii=True) + "\n").encode("utf-8")
            write_output(pretty, args.output)
            return 0

        write_output(body, args.output)
        return 0

    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        print(f"HTTP {exc.code}: {detail}", file=sys.stderr)
        return 1
    except URLError as exc:
        print(f"Request failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
