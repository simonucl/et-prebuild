# test_initial_state.py
#
# Pytest suite that validates the initial filesystem state **before**
# any encryption command is run for the task described in the prompt.
#
# Preconditions checked:
#   1. The directory /home/user/experiments/run_15 exists and is a directory.
#   2. It is writable by the current user (0700 expected).
#   3. The file /home/user/experiments/run_15/metrics.json exists,
#      is readable, non-empty, and contains the expected JSON with:
#         {"accuracy": 0.953, "loss": 0.127}
#      (ignoring insignificant whitespace, but a single trailing newline
#       after the closing brace is required).
#   4. No encrypted file or log file is present yet:
#         /home/user/experiments/run_15/metrics.json.gpg
#         /home/user/experiments/run_15/encryption_log.txt
#   5. No *extra* files are present inside run_15/—only metrics.json must
#      exist at task start.
#
# Failures provide clear messages telling the student exactly what is
# missing or unexpected.

import json
import os
import stat
from pathlib import Path

import pytest

RUN15_DIR = Path("/home/user/experiments/run_15")
METRICS_JSON = RUN15_DIR / "metrics.json"
ENCRYPTED_FILE = RUN15_DIR / "metrics.json.gpg"
LOG_FILE = RUN15_DIR / "encryption_log.txt"


def _octal_permissions(path: Path) -> str:
    """
    Return the permission bits of `path` as a string in octal notation,
    e.g. '0700' or '0600'.
    """
    return oct(path.stat().st_mode & 0o777)


def test_run15_directory_exists_and_permissions():
    assert RUN15_DIR.exists(), (
        f"Required directory {RUN15_DIR} is missing.\n"
        "Create it before running your encryption command."
    )
    assert RUN15_DIR.is_dir(), f"{RUN15_DIR} exists but is not a directory."

    perms = _octal_permissions(RUN15_DIR)
    expected = "0o700"
    assert perms == expected, (
        f"Directory {RUN15_DIR} should have permissions {expected} "
        f"but has {perms}. Fix the permissions."
    )


def test_metrics_json_exists_and_content():
    assert METRICS_JSON.exists(), (
        f"Required file {METRICS_JSON} is missing.\n"
        "It must exist before you perform the encryption step."
    )
    assert METRICS_JSON.is_file(), f"{METRICS_JSON} exists but is not a regular file."
    assert METRICS_JSON.stat().st_size > 0, f"{METRICS_JSON} is empty; expected JSON data."

    perms = _octal_permissions(METRICS_JSON)
    expected = "0o600"
    assert perms == expected, (
        f"File {METRICS_JSON} should have permissions {expected} "
        f"but has {perms}. Fix the permissions."
    )

    raw_text = METRICS_JSON.read_text(encoding="utf-8")
    assert raw_text.endswith("\n"), (
        f"{METRICS_JSON} must end with exactly one newline character."
    )

    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        pytest.fail(f"{METRICS_JSON} does not contain valid JSON: {exc}")

    expected_data = {"accuracy": 0.953, "loss": 0.127}
    assert data == expected_data, (
        f"{METRICS_JSON} JSON content mismatch.\n"
        f"Expected: {expected_data}\n"
        f"Found:    {data}"
    )


def test_encrypted_and_log_files_absent():
    assert not ENCRYPTED_FILE.exists(), (
        f"{ENCRYPTED_FILE} already exists, but it should not be present "
        "before running your encryption command."
    )
    assert not LOG_FILE.exists(), (
        f"{LOG_FILE} already exists, but it should not be present "
        "before running your encryption command."
    )


def test_no_extra_files_present():
    present_files = sorted(p.name for p in RUN15_DIR.iterdir() if p.is_file())
    expected_files = ["metrics.json"]
    extra_files = [f for f in present_files if f not in expected_files]
    assert not extra_files, (
        f"Unexpected extra files found in {RUN15_DIR}: {extra_files}\n"
        "Only metrics.json should be present before the task starts."
    )