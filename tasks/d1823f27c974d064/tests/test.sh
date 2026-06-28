#!/bin/bash
set -u

mkdir -p /logs/verifier

python3 - <<'PY'
import hashlib
import json
import os
import re
import subprocess
import sys
import tarfile
from pathlib import Path

repo = Path("/home/circleci/widget-service")
release_dir = Path("/home/circleci/releases")
archive_name = "widget-service-1.4.2.tar.gz"
archive = release_dir / archive_name
manifest = release_dir / "widget-service-1.4.2.manifest.json"
reward_path = Path("/logs/verifier/reward.txt")


def fail(message):
    print(message)
    reward_path.write_text("0\n")
    sys.exit(0)


def run_git(*args):
    try:
        return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()
    except subprocess.CalledProcessError as exc:
        fail(f"git command failed: {' '.join(args)}: {exc}")


if not repo.is_dir():
    fail("repository is missing")
if not archive.is_file():
    fail("release archive is missing")
if not manifest.is_file():
    fail("manifest is missing")

try:
    head = run_git("rev-parse", "HEAD")
except Exception as exc:
    fail(f"could not read HEAD: {exc}")

if not re.fullmatch(r"[0-9a-f]{40}", head):
    fail("HEAD is not a full commit hash")

try:
    attrs = (repo / ".gitattributes").read_text()
except FileNotFoundError:
    fail(".gitattributes is missing")

required_attr_lines = [
    "tests/ export-ignore",
    "docs/draft.md export-ignore",
    ".env.sample export-ignore",
    ".ci/ export-ignore",
    "build/ export-ignore",
]
attr_lines = [line.strip() for line in attrs.splitlines() if line.strip()]
for line in required_attr_lines:
    if line not in attr_lines:
        fail(f"missing attribute rule: {line}")

tracked_blob = run_git("show", "HEAD:.gitattributes")
for line in required_attr_lines:
    if line not in [item.strip() for item in tracked_blob.splitlines() if item.strip()]:
        fail(".gitattributes rules were not committed before archiving")

try:
    with tarfile.open(archive, "r:gz") as tf:
        members = tf.getmembers()
        file_entries = sorted(member.name for member in members if member.isfile())
        file_payloads = {
            member.name: tf.extractfile(member).read()
            for member in members
            if member.isfile()
        }
        all_entries = [
            member.name
            for member in members
            if member.isfile() or member.isdir() or member.issym()
        ]
except Exception as exc:
    fail(f"archive is not a readable gzip tar: {exc}")

prefix = "widget-service-1.4.2/"
top = prefix.rstrip("/")
if not all(name == top or name == prefix or name.startswith(prefix) for name in all_entries):
    fail(f"archive entries do not all use the required prefix: {all_entries!r}")

for forbidden in [
    "widget-service-1.4.2/tests/",
    "widget-service-1.4.2/docs/draft.md",
    "widget-service-1.4.2/.env.sample",
    "widget-service-1.4.2/.ci/",
    "widget-service-1.4.2/build/",
]:
    if any(name == forbidden or name.startswith(forbidden) for name in all_entries):
        fail(f"archive contains excluded path: {forbidden}")

expected_files = [
    "widget-service-1.4.2/.gitattributes",
    "widget-service-1.4.2/README.md",
    "widget-service-1.4.2/pyproject.toml",
    "widget-service-1.4.2/scripts/healthcheck.sh",
    "widget-service-1.4.2/src/widget_service/__init__.py",
    "widget-service-1.4.2/src/widget_service/cli.py",
]
if file_entries != expected_files:
    fail(f"archive regular-file entries differ: {file_entries!r}")

for entry in expected_files:
    repo_path = entry.removeprefix(prefix)
    expected_blob = subprocess.check_output(
        ["git", "-C", str(repo), "show", f"HEAD:{repo_path}"]
    )
    if file_payloads[entry] != expected_blob:
        fail(f"archive content does not match HEAD for {entry}")

raw_manifest = manifest.read_text()
if not raw_manifest.endswith("\n") or raw_manifest.count("\n") != 1:
    fail("manifest must be one minified JSON line with one trailing newline")
if " " in raw_manifest or "\t" in raw_manifest:
    fail("manifest contains whitespace outside the trailing newline")

pairs = json.loads(raw_manifest, object_pairs_hook=list)
top_keys = [key for key, _ in pairs]
expected_keys = ["package", "version", "git_commit", "archive", "sha256", "size_bytes", "entries"]
if top_keys != expected_keys:
    fail(f"manifest keys are out of order: {top_keys!r}")
data = dict(pairs)

expected_manifest = {
    "package": "widget-service",
    "version": "1.4.2",
    "git_commit": head,
    "archive": archive_name,
    "sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
    "size_bytes": os.path.getsize(archive),
    "entries": expected_files,
}

if data != expected_manifest:
    fail(f"manifest values are incorrect: {data!r}")

if raw_manifest != json.dumps(expected_manifest, separators=(",", ":")) + "\n":
    fail("manifest is not canonical minified JSON")

reward_path.write_text("1\n")
PY
