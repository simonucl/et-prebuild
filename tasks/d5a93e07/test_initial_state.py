# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the operating-system
# filesystem **before** the student runs the one-liner command required by the
# assignment.  If any of these tests fail, the environment is not in the
# expected clean state and the assignment cannot be graded reliably.

import json
import re
import stat
from pathlib import Path

import pytest


DATA_DIR      = Path("/home/user/data")
JSON_FILE     = DATA_DIR / "release_config.json"
LOGS_DIR      = Path("/home/user/logs")
OUTPUT_FILE   = LOGS_DIR / "version_mismatch.log"


# --------------------------------------------------------------------------- #
# 1. Basic presence / absence checks
# --------------------------------------------------------------------------- #

def test_data_directory_exists():
    assert DATA_DIR.is_dir(), (
        f"Required directory {DATA_DIR} is missing.  "
        "The assignment expects this directory to exist before any action "
        "is taken."
    )


def test_release_config_json_exists():
    assert JSON_FILE.is_file(), (
        f"Required file {JSON_FILE} is missing.  "
        "The student’s command must read this file with jq."
    )


def test_logs_directory_absent_initially():
    assert not LOGS_DIR.exists(), (
        f"Directory {LOGS_DIR} should NOT exist before the student runs the "
        "task.  Initial state must be clean so that the command has to "
        "create it."
    )


def test_output_file_absent_initially():
    assert not OUTPUT_FILE.exists(), (
        f"File {OUTPUT_FILE} should NOT exist before the student runs the "
        "task.  It must be produced by their command."
    )


# --------------------------------------------------------------------------- #
# 2. Detailed inspection of release_config.json
# --------------------------------------------------------------------------- #

EXPECTED_JSON = [
    {"service": "auth",    "version": "v1.2.0", "port": 8000},
    {"service": "billing", "version": "1.0.0",  "port": 8010},
    {"service": "search",  "version": "v2.0.1", "port": 8020},
    {"service": "legacy",  "version": "v3.0",   "port": 8030},
    {"service": "reports", "version": "v4.1.0", "port": 8040},
]


def _load_release_config():
    try:
        with JSON_FILE.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError as exc:
        pytest.fail(f"{JSON_FILE} is not valid JSON: {exc}")  # pragma: no cover


def test_release_config_json_content():
    data = _load_release_config()
    assert data == EXPECTED_JSON, (
        f"The contents of {JSON_FILE} do not match the expected initial "
        "configuration.  Grading depends on the exact data shown in the task "
        "description."
    )


# --------------------------------------------------------------------------- #
# 3. Sanity-check the number of non-conforming semantic versions
# --------------------------------------------------------------------------- #

SEMVER_PATTERN = re.compile(r"^v\d+\.\d+\.\d+$")


def test_non_conforming_count_is_two():
    """
    Quick sanity check: exactly two objects ('billing' and 'legacy') should
    have versions that do NOT match the pattern  ^vMAJOR.MINOR.PATCH$ .
    """
    data = _load_release_config()
    non_conforming = [
        entry for entry in data
        if not SEMVER_PATTERN.match(entry.get("version", ""))
    ]
    assert len(non_conforming) == 2, (
        "Based on the initial JSON, there should be exactly two services whose "
        "version fields do not conform to the required semantic-version "
        "pattern.  Found "
        f"{len(non_conforming)} invalid entries: {non_conforming}"
    )


# --------------------------------------------------------------------------- #
# 4. Optional permission checks (not strictly required but helpful)
# --------------------------------------------------------------------------- #

def test_permissions_on_data_and_json():
    data_mode = DATA_DIR.stat().st_mode
    json_mode = JSON_FILE.stat().st_mode
    assert stat.S_IMODE(data_mode) & 0o777 == 0o755, (
        f"Directory {DATA_DIR} should have permissions 0755."
    )
    assert stat.S_IMODE(json_mode) & 0o777 == 0o644, (
        f"File {JSON_FILE} should have permissions 0644."
    )