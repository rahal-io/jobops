#!/usr/bin/env python3
"""Lint or bundle all domain specs listed in domains.json."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "domains.json"
SRC = ROOT / "src"
BUNDLED = SRC / ".bundled"
REDOCLY_CONFIG = ROOT / ".redocly.yaml"


def load_domains() -> list[dict]:
    if not CONFIG.exists():
        print(f"Config not found: {CONFIG}", file=sys.stderr)
        sys.exit(1)
    with open(CONFIG, encoding="utf-8") as f:
        data = json.load(f)
    out = []
    for d in data.get("domains") or []:
        spec_name = (d.get("spec_path") or "").strip()
        bundled_name = (d.get("bundled_path") or "").strip()
        if not spec_name or not bundled_name:
            continue
        out.append(
            {
                "name": d.get("name", ""),
                "spec_path": SRC / spec_name,
                "bundled_path": BUNDLED / bundled_name,
            }
        )
    return out


def run_lint(domains: list[dict]) -> None:
    specs = [str(d["spec_path"]) for d in domains]
    if not specs:
        print("No domains configured.", file=sys.stderr)
        sys.exit(1)
    cmd = ["pnpm", "-s", "redocly", "lint", "--config", str(REDOCLY_CONFIG), *specs]
    result = subprocess.run(cmd, cwd=str(ROOT))
    sys.exit(result.returncode)


def run_bundle(domains: list[dict]) -> None:
    for d in domains:
        spec = d["spec_path"]
        out = d["bundled_path"]
        if not spec.exists():
            print(f"Spec not found: {spec}", file=sys.stderr)
            sys.exit(1)
        out.parent.mkdir(parents=True, exist_ok=True)
        cmd = [
            "pnpm",
            "-s",
            "exec",
            "redocly",
            "bundle",
            str(spec),
            "--dereferenced",
            "-o",
            str(out),
            "--force",
        ]
        result = subprocess.run(cmd, cwd=str(ROOT))
        if result.returncode != 0:
            sys.exit(result.returncode)
    print(f"Bundled {len(domains)} domains.")


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in ("lint", "bundle"):
        print("Usage: lint_and_bundle_from_config.py lint | bundle", file=sys.stderr)
        sys.exit(1)
    domains = load_domains()
    if sys.argv[1] == "lint":
        run_lint(domains)
    else:
        run_bundle(domains)


if __name__ == "__main__":
    main()
