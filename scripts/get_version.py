#!/usr/bin/env python3
"""Fetch ClinicalTrials.gov API version metadata."""

import argparse
import json
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_URL = "https://clinicaltrials.gov/api/v2/version"
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
    parser = argparse.ArgumentParser(description="Fetch API version metadata")
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    parser.add_argument("--output", help="Write output bytes to file")
    args = parser.parse_args()

    try:
        body, content_type = fetch(args.url)
        if args.pretty and "json" in content_type.lower():
            parsed = json.loads(body.decode("utf-8"))
            body = (json.dumps(parsed, indent=2, ensure_ascii=True) + "\n").encode("utf-8")

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
