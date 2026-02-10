#!/usr/bin/env python3
"""Fetch one ClinicalTrials.gov study by NCT ID via API v2."""

import argparse
import json
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

DEFAULT_BASE_URL = "https://clinicaltrials.gov/api/v2/studies"
USER_AGENT = "clinicaltrials-gov-api-skill/1.0"


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
    parser = argparse.ArgumentParser(description="Fetch one study by NCT ID")
    parser.add_argument("nct_id", help="Example: NCT04280705")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--format", choices=["json", "csv"], default="json")
    parser.add_argument("--field", dest="fields", action="append", help="fields (repeatable field path)")
    parser.add_argument("--raw-url", action="store_true", help="Print the final URL to stderr")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    parser.add_argument("--output", help="Write output bytes to file")
    args = parser.parse_args()

    params = {"format": args.format}
    if args.fields:
        params["fields"] = ",".join(args.fields)

    study_path = quote(args.nct_id)
    base = f"{args.base_url.rstrip('/')}/{study_path}"
    url = f"{base}?{urlencode(params)}"

    if args.raw_url:
        print(url, file=sys.stderr)

    try:
        body, content_type = fetch(url)
        if args.format == "json" and "json" in content_type.lower() and args.pretty:
            parsed = json.loads(body.decode("utf-8"))
            pretty = (json.dumps(parsed, indent=2, ensure_ascii=True) + "\n").encode("utf-8")
            write_output(pretty, args.output)
            return 0

        write_output(body, args.output)
        return 0

    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        print(f"HTTP {exc.code}: {detail}", file=sys.stderr)
        return 1
    except URLError as exc:
        print(f"Request failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
