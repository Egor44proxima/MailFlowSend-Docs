#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import os
import pathlib
import sys
import urllib.error
import urllib.request

DEFAULT_BASELINE = pathlib.Path("docs/_meta/source-baseline.json")
DEFAULT_OUTPUT = pathlib.Path("docs/assets/source-status.json")

def load_baseline(path: pathlib.Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    required = {
        "source_repository",
        "source_branch",
        "documented_source_sha",
        "core",
        "schema",
        "abi",
        "migration",
        "documented_at",
    }
    missing = sorted(required - set(data))
    if missing:
        raise RuntimeError("baseline missing fields: " + ", ".join(missing))
    sha = str(data["documented_source_sha"]).strip()
    if len(sha) != 40 or any(ch not in "0123456789abcdef" for ch in sha.lower()):
        raise RuntimeError("documented_source_sha must be a full 40-character SHA")
    return data

def query_source_head(repo: str, branch: str, token: str) -> str:
    url = f"https://api.github.com/repos/{repo}/branches/{branch}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "MailFlowSend-Docs-Freshness",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.load(resp)
    sha = str(data["commit"]["sha"]).strip()
    if len(sha) != 40:
        raise RuntimeError("GitHub returned an invalid branch SHA")
    return sha

def main() -> int:
    parser = argparse.ArgumentParser(description="Compare documented MailFlowSend source SHA with live main.")
    parser.add_argument("--baseline", default=str(DEFAULT_BASELINE))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--strict", action="store_true", help="Exit non-zero unless status is CURRENT.")
    parser.add_argument("--check-only", action="store_true", help="Do not write public JSON status.")
    args = parser.parse_args()

    baseline_path = pathlib.Path(args.baseline)
    output_path = pathlib.Path(args.output)
    baseline = load_baseline(baseline_path)

    token = os.environ.get("MAILFLOWSEND_SOURCE_TOKEN", "").strip()
    checked_at = dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")
    docs_sha = os.environ.get("GITHUB_SHA", "").strip()
    current_sha = ""
    status = "UNKNOWN"
    reason = ""

    try:
        if not token:
            raise RuntimeError("MAILFLOWSEND_SOURCE_TOKEN is not configured")
        current_sha = query_source_head(
            str(baseline["source_repository"]),
            str(baseline["source_branch"]),
            token,
        )
        if current_sha == baseline["documented_source_sha"]:
            status = "CURRENT"
            reason = "Documentation baseline matches MailFlowSend/main."
        else:
            status = "OUTDATED"
            reason = "MailFlowSend/main has advanced beyond the documented source baseline."
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, RuntimeError, KeyError, ValueError) as exc:
        status = "UNKNOWN"
        reason = f"Freshness check unavailable: {exc}"

    public = {
        "status": status,
        "source_repository": baseline["source_repository"],
        "source_branch": baseline["source_branch"],
        "documented_source_sha": baseline["documented_source_sha"],
        "current_source_sha": current_sha,
        "docs_sha": docs_sha,
        "checked_at": checked_at,
        "core": baseline["core"],
        "schema": baseline["schema"],
        "abi": baseline["abi"],
        "migration": baseline["migration"],
        "documented_at": baseline["documented_at"],
        "reason": reason,
    }

    print(f"DOCS FRESHNESS: {status}")
    print(f"documented_source_sha={baseline['documented_source_sha']}")
    print(f"current_source_sha={current_sha or 'unavailable'}")
    print(reason)

    if not args.check_only:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(public, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    if args.strict and status != "CURRENT":
        return 2
    return 0

if __name__ == "__main__":
    sys.exit(main())
