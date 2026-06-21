# test_initial_state.py
#
# Pytest suite that validates the **initial** filesystem state *before* the
# student starts working on the “Grafana dashboard integrity” task.
#
# Expectations derived from the task description & hidden truth value:
#
#   /home/user/dashboards
#   ├── backups
#   │   ├── app_latency.json       (empty file, SHA256 == EMPTY_FILE_SHA)
#   │   ├── error_rate.json        (empty file, SHA256 == EMPTY_FILE_SHA)
#   │   ├── infra_overview.json    (empty file, SHA256 == EMPTY_FILE_SHA)
#   │   └── business_kpis.json     (empty file, SHA256 == EMPTY_FILE_SHA)
#   ├── staging
#   │   ├── app_latency.json       (corrupted, single byte "a", SHA256 == SINGLE_A_SHA)
#   │   ├── error_rate.json        (empty file, SHA256 == EMPTY_FILE_SHA)
#   │   ├── infra_overview.json    (empty file, SHA256 == EMPTY_FILE_SHA)
#   │   └── business_kpis.json     (empty file, SHA256 == EMPTY_FILE_SHA)
#   └── manifest.sha256            (lists EMPTY_FILE_SHA for **all** four files)
#
# No integrity_audit.log is present yet.
#
# Any deviation from this baseline means the exercise cannot be graded
# reliably, so the tests fail with a clear explanation.

import hashlib
import os
from pathlib import Path

import pytest

HOME = Path("/home/user").resolve()
DASH_ROOT = HOME / "dashboards"
STAGING_DIR = DASH_ROOT / "staging"
BACKUP_DIR = DASH_ROOT / "backups"
MANIFEST = DASH_ROOT / "manifest.sha256"
AUDIT_LOG = DASH_ROOT / "integrity_audit.log"

FILENAMES = [
    "app_latency.json",
    "error_rate.json",
    "infra_overview.json",
    "business_kpis.json",
]

# Known SHA-256 digests
EMPTY_FILE_SHA = (
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
)  # 0-byte file
SINGLE_A_SHA = (
    "ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb"
)  # file with single letter "a"


def sha256_of_file(path: Path) -> str:
    """Return SHA-256 hex digest of the given file."""
    h = hashlib.sha256()
    with path.open("rb") as fp:
        for chunk in iter(lambda: fp.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Directory and file presence
# ---------------------------------------------------------------------------


def test_required_directories_exist():
    assert STAGING_DIR.is_dir(), f"Missing staging directory: {STAGING_DIR}"
    assert BACKUP_DIR.is_dir(), f"Missing backup directory: {BACKUP_DIR}"


def test_required_files_exist():
    # Manifest
    assert MANIFEST.is_file(), f"Missing checksum manifest: {MANIFEST}"

    # Dashboard JSON files in staging & backups
    missing_staging = [f for f in FILENAMES if not (STAGING_DIR / f).is_file()]
    missing_backups = [f for f in FILENAMES if not (BACKUP_DIR / f).is_file()]

    assert not missing_staging, (
        "Staging directory is missing the following files: "
        + ", ".join(missing_staging)
    )
    assert not missing_backups, (
        "Backup directory is missing the following files: "
        + ", ".join(missing_backups)
    )


def test_audit_log_absent():
    assert not AUDIT_LOG.exists(), (
        f"{AUDIT_LOG} must NOT exist before the student runs their solution."
    )


# ---------------------------------------------------------------------------
# Manifest content
# ---------------------------------------------------------------------------


def test_manifest_has_expected_content():
    """The manifest must list exactly four files with the EMPTY_FILE_SHA digest."""
    lines = MANIFEST.read_text(encoding="utf-8").rstrip("\n").splitlines()
    assert (
        len(lines) == 4
    ), f"Manifest should have 4 lines, found {len(lines)} line(s). Got: {lines!r}"

    seen_files = set()
    for idx, line in enumerate(lines, 1):
        # sha256sum output format is: <digest><2 spaces><filename>\n
        parts = line.strip().split()  # split on any whitespace
        assert (
            len(parts) == 2
        ), f"Line {idx} in manifest should have 2 whitespace-separated fields, got: {line!r}"
        digest, filename = parts
        assert (
            digest == EMPTY_FILE_SHA
        ), f"Line {idx}: digest should be EMPTY_FILE_SHA ({EMPTY_FILE_SHA}), got {digest}"
        assert (
            filename in FILENAMES
        ), f"Line {idx}: unexpected filename '{filename}' in manifest"
        seen_files.add(filename)

    missing = set(FILENAMES) - seen_files
    assert not missing, f"Manifest missing entries for: {', '.join(sorted(missing))}"


# ---------------------------------------------------------------------------
# File contents / checksums
# ---------------------------------------------------------------------------


def test_staging_app_latency_is_corrupted():
    """staging/app_latency.json is intentionally corrupted with a single 'a' byte."""
    path = STAGING_DIR / "app_latency.json"
    assert path.stat().st_size == 1, (
        "staging/app_latency.json should be 1 byte (single 'a'), "
        f"but is {path.stat().st_size} bytes."
    )

    digest = sha256_of_file(path)
    assert (
        digest == SINGLE_A_SHA
    ), f"staging/app_latency.json SHA-256 should be {SINGLE_A_SHA}, got {digest}"


@pytest.mark.parametrize(
    "filename",
    [
        "error_rate.json",
        "infra_overview.json",
        "business_kpis.json",
    ],
)
def test_other_staging_files_are_empty_and_match_manifest(filename):
    """Remaining staging files must be 0 bytes and match EMPTY_FILE_SHA."""
    path = STAGING_DIR / filename
    assert path.stat().st_size == 0, (
        f"staging/{filename} should be empty (0 bytes), "
        f"but size is {path.stat().st_size} bytes."
    )
    digest = sha256_of_file(path)
    assert (
        digest == EMPTY_FILE_SHA
    ), f"staging/{filename} SHA-256 should be {EMPTY_FILE_SHA}, got {digest}"


@pytest.mark.parametrize("filename", FILENAMES)
def test_backup_files_are_empty_and_match_manifest(filename):
    """All backup files are pristine (0-byte) copies with the EMPTY_FILE_SHA digest."""
    path = BACKUP_DIR / filename
    assert path.stat().st_size == 0, (
        f"backups/{filename} should be empty (0 bytes), "
        f"but size is {path.stat().st_size} bytes."
    )
    digest = sha256_of_file(path)
    assert (
        digest == EMPTY_FILE_SHA
    ), f"backups/{filename} SHA-256 should be {EMPTY_FILE_SHA}, got {digest}"