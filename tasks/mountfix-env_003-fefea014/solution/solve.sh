#!/bin/bash
set -euo pipefail

cd /home/user/reconcilor

python3 - <<'PY'
from pathlib import Path

Path("pyproject.toml").write_text('''[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"

[project]
name = "stale-reporter"
version = "0.1.0"
description = "Offline stale asset reporter"
requires-python = ">=3.11"

[project.scripts]
stale-report = "stale_reporter.cli:main"
''')

Path("setup.py").write_text('''import setuptools

setuptools.setup(
    name="stale-reporter",
    version="0.1.0",
    package_dir={"": "src"},
    packages=setuptools.find_packages("src"),
    entry_points={"console_scripts": ["stale-report=stale_reporter.cli:main"]},
)
''')

Path("src/stale_reporter/cli.py").write_text('''from __future__ import annotations

import argparse
import csv
import json
from datetime import date
from pathlib import Path


RETENTION_DAYS = {
    "prod": 90,
    "archive": 365,
    "ephemeral": None,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build stale asset manifests.")
    parser.add_argument("--data-dir", default="/home/user/reconcilor/data")
    parser.add_argument("--output-dir", default="/home/user/reconcilor/out")
    parser.add_argument("--as-of", required=True)
    return parser.parse_args()


def load_checksums(path: Path) -> dict[str, str]:
    checksums: dict[str, str] = {}
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        digest, asset_path = line.split(None, 1)
        checksums[asset_path.strip()] = digest
    return checksums


def stale_threshold(classification: str) -> int | None:
    return RETENTION_DAYS.get(classification, 180)


def build_rows(data_dir: Path, as_of: date) -> list[dict[str, object]]:
    checksums = load_checksums(data_dir / "checksums.sha256")
    stale_rows: list[dict[str, object]] = []
    with (data_dir / "inventory.csv").open(newline="") as fh:
        for row in csv.DictReader(fh):
            threshold = stale_threshold(row["classification"])
            if threshold is None:
                continue
            age_days = (as_of - date.fromisoformat(row["last_seen"])).days
            if age_days > threshold:
                asset_path = row["path"]
                stale_rows.append(
                    {
                        "path": asset_path,
                        "owner": row["owner"],
                        "last_seen": row["last_seen"],
                        "classification": row["classification"],
                        "age_days": age_days,
                        "sha256": checksums.get(asset_path),
                    }
                )
    stale_rows.sort(key=lambda item: (str(item["owner"]), str(item["path"])))
    return stale_rows


def write_outputs(out_dir: Path, as_of_text: str, rows: list[dict[str, object]]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    owners = sorted({str(row["owner"]) for row in rows})
    missing = sum(1 for row in rows if row["sha256"] is None)
    payload = {
        "as_of": as_of_text,
        "summary": {
            "stale_count": len(rows),
            "missing_checksum_count": missing,
            "owners": owners,
        },
        "stale_assets": rows,
    }
    (out_dir / "stale_manifest.json").write_text(
        json.dumps(payload, separators=(",", ":")) + "\\n"
    )
    lines = ["owner\\tpath\\tage_days\\tclassification\\tsha256"]
    for row in rows:
        checksum = row["sha256"] if row["sha256"] is not None else "MISSING"
        lines.append(
            f'{row["owner"]}\\t{row["path"]}\\t{row["age_days"]}\\t{row["classification"]}\\t{checksum}'
        )
    (out_dir / "stale_manifest.tsv").write_text("\\n".join(lines) + "\\n")


def main() -> int:
    args = parse_args()
    as_of = date.fromisoformat(args.as_of)
    rows = build_rows(Path(args.data_dir), as_of)
    write_outputs(Path(args.output_dir), args.as_of, rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
''')
PY

python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install --no-index --no-build-isolation -e .
stale-report --data-dir /home/user/reconcilor/data --output-dir /home/user/reconcilor/out --as-of 2024-04-15
