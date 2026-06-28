#!/bin/bash
set -u

mkdir -p /logs/verifier
cd /home/user/reconcilor || {
  echo 0 > /logs/verifier/reward.txt
  exit 1
}

python3 - <<'PY'
from __future__ import annotations

import csv
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import tomllib
from datetime import date
from pathlib import Path

REPO = Path("/home/user/reconcilor")
DATA = REPO / "data"
OUT = REPO / "out"
REWARD = Path("/logs/verifier/reward.txt")


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    REWARD.write_text("0\n")
    raise SystemExit(1)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def expected(data_dir: Path, as_of_text: str):
    as_of = date.fromisoformat(as_of_text)
    checksums = {}
    for raw_line in (data_dir / "checksums.sha256").read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        digest, asset_path = line.split(None, 1)
        checksums[asset_path.strip()] = digest

    rows = []
    thresholds = {"prod": 90, "archive": 365, "ephemeral": None}
    with (data_dir / "inventory.csv").open(newline="") as fh:
        for row in csv.DictReader(fh):
            threshold = thresholds.get(row["classification"], 180)
            if threshold is None:
                continue
            age_days = (as_of - date.fromisoformat(row["last_seen"])).days
            if age_days > threshold:
                asset_path = row["path"]
                rows.append(
                    {
                        "path": asset_path,
                        "owner": row["owner"],
                        "last_seen": row["last_seen"],
                        "classification": row["classification"],
                        "age_days": age_days,
                        "sha256": checksums.get(asset_path),
                    }
                )
    rows.sort(key=lambda item: (item["owner"], item["path"]))
    payload = {
        "as_of": as_of_text,
        "summary": {
            "stale_count": len(rows),
            "missing_checksum_count": sum(1 for row in rows if row["sha256"] is None),
            "owners": sorted({row["owner"] for row in rows}),
        },
        "stale_assets": rows,
    }
    tsv_lines = ["owner\tpath\tage_days\tclassification\tsha256"]
    for row in rows:
        tsv_lines.append(
            "\t".join(
                [
                    row["owner"],
                    row["path"],
                    str(row["age_days"]),
                    row["classification"],
                    row["sha256"] if row["sha256"] is not None else "MISSING",
                ]
            )
        )
    return json.dumps(payload, separators=(",", ":")) + "\n", "\n".join(tsv_lines) + "\n"


try:
    pyproject = tomllib.loads((REPO / "pyproject.toml").read_text())
except Exception as exc:
    fail(f"pyproject.toml is not valid TOML: {exc}")

script_target = pyproject.get("project", {}).get("scripts", {}).get("stale-report")
if script_target != "stale_reporter.cli:main":
    fail("pyproject.toml must define stale-report = stale_reporter.cli:main")

before_hashes = {path.name: sha256(path) for path in DATA.iterdir() if path.is_file()}

venv = Path(tempfile.mkdtemp(prefix="stale-report-venv-"))
try:
    subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True)
    pip = venv / "bin" / "pip"
    stale_report = venv / "bin" / "stale-report"
    subprocess.run([str(pip), "install", "--no-index", "--no-build-isolation", "-e", str(REPO)], check=True)

    shutil.rmtree(OUT, ignore_errors=True)
    subprocess.run(
        [
            str(stale_report),
            "--data-dir",
            str(DATA),
            "--output-dir",
            str(OUT),
            "--as-of",
            "2024-04-15",
        ],
        check=True,
    )

    exp_json, exp_tsv = expected(DATA, "2024-04-15")
    if (OUT / "stale_manifest.json").read_text() != exp_json:
        fail("staged stale_manifest.json does not match expected minified content")
    if (OUT / "stale_manifest.tsv").read_text() != exp_tsv:
        fail("staged stale_manifest.tsv does not match expected TSV content")

    after_hashes = {path.name: sha256(path) for path in DATA.iterdir() if path.is_file()}
    if after_hashes != before_hashes:
        fail("source data files under data/ were modified")

    with tempfile.TemporaryDirectory(prefix="stale-fixture-") as tmp:
        tmp_path = Path(tmp)
        fixture_data = tmp_path / "data"
        fixture_out = tmp_path / "out"
        fixture_data.mkdir()
        (fixture_data / "inventory.csv").write_text(
            "path,owner,last_seen,classification\n"
            "ops/runbook.md,team-ops,2024-02-01,other\n"
            "ml/model.bin,team-ml,2023-01-02,archive\n"
            "ml/current.bin,team-ml,2024-05-01,archive\n"
            "api/ancient.cfg,team-api,2024-01-30,prod\n"
            "tmp/cache.bin,team-api,2022-01-01,ephemeral\n"
        )
        (fixture_data / "checksums.sha256").write_text(
            "# alternate fixture\n"
            "1111111111111111111111111111111111111111111111111111111111111111  ops/runbook.md\n"
            "2222222222222222222222222222222222222222222222222222222222222222  ml/model.bin\n"
            "3333333333333333333333333333333333333333333333333333333333333333  ml/current.bin\n"
        )
        subprocess.run(
            [
                str(stale_report),
                "--data-dir",
                str(fixture_data),
                "--output-dir",
                str(fixture_out),
                "--as-of",
                "2024-06-01",
            ],
            check=True,
        )
        exp_json, exp_tsv = expected(fixture_data, "2024-06-01")
        if (fixture_out / "stale_manifest.json").read_text() != exp_json:
            fail("fresh fixture JSON output is not computed correctly")
        if (fixture_out / "stale_manifest.tsv").read_text() != exp_tsv:
            fail("fresh fixture TSV output is not computed correctly")
finally:
    shutil.rmtree(venv, ignore_errors=True)

REWARD.write_text("1\n")
PY

status=$?
if [ "$status" -ne 0 ]; then
  [ -s /logs/verifier/reward.txt ] || echo 0 > /logs/verifier/reward.txt
  exit "$status"
fi
