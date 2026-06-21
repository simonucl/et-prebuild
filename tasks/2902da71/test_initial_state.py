# test_initial_state.py
#
# This test-suite verifies that the operating-system state **before** the
# student starts working is exactly as described in the task specification.
#
# The checks are deliberately strict—any deviation will produce a clear,
# actionable failure message.

import json
import os
import stat
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Helper constants
# --------------------------------------------------------------------------- #

HOME = Path("/home/user").resolve()
DATA_DIR = HOME / "data"
SCHEMAS_DIR = HOME / "schemas"
OUTPUT_DIR = HOME / "output"

PING_RESULTS_FILE = DATA_DIR / "ping_results.json"
PING_SCHEMA_FILE = SCHEMAS_DIR / "ping_result.schema.json"

# Expected raw content for ping_results.json (order and spacing ignored,
# logical equality enforced via JSON parsing).
EXPECTED_PING_RESULTS = [
    {"host": "db-1",  "timestamp": "2023-08-01T10:00:00Z", "status": "up",   "latency_ms": 45},
    {"host": "db-1",  "timestamp": "2023-08-01T10:05:00Z", "status": "up",   "latency_ms": 50},
    {"host": "db-1",  "timestamp": "2023-08-01T10:10:00Z", "status": "up",   "latency_ms": 47},
    {"host": "db-1",  "timestamp": "2023-08-01T10:15:00Z", "status": "up",   "latency_ms": 46},
    {"host": "web-1", "timestamp": "2023-08-01T10:00:00Z", "status": "up",   "latency_ms": 23},
    {"host": "web-1", "timestamp": "2023-08-01T10:05:00Z", "status": "down", "latency_ms": None},
    {"host": "web-1", "timestamp": "2023-08-01T10:10:00Z", "status": "up",   "latency_ms": 25},
    {"host": "web-1", "timestamp": "2023-08-01T10:15:00Z", "status": "up",   "latency_ms": 22},
]

# Expected raw content for ping_result.schema.json (order of keys within the
# JSON object is irrelevant; numerical equality is enforced).
EXPECTED_PING_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "array",
    "items": {
        "type": "object",
        "required": ["host", "timestamp", "status", "latency_ms"],
        "properties": {
            "host": {"type": "string"},
            "timestamp": {"type": "string"},
            "status": {"type": "string", "enum": ["up", "down"]},
            "latency_ms": {"type": ["number", "null"]},
        },
        "additionalProperties": False,
    },
}


# --------------------------------------------------------------------------- #
# Utility helpers
# --------------------------------------------------------------------------- #
def _mode(path: Path) -> int:
    """Return Unix permissions bits for the given path."""
    return stat.S_IMODE(path.stat().st_mode)


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_directories_present_and_permissions():
    """data/ and schemas/ directories must exist; output/ must not yet exist."""
    assert DATA_DIR.is_dir(), f"Missing directory: {DATA_DIR}"
    assert SCHEMAS_DIR.is_dir(), f"Missing directory: {SCHEMAS_DIR}"

    # Permissions (755)
    for d in (DATA_DIR, SCHEMAS_DIR):
        perms = _mode(d)
        assert perms == 0o755, (
            f"Directory {d} should have permissions 755, found {oct(perms)}"
        )

    # output directory must *not* exist before the student runs their solution
    assert not OUTPUT_DIR.exists(), (
        "Directory /home/user/output should not exist initially; "
        "it must be created by the student's solution."
    )


def test_ping_results_file_and_permissions():
    """ping_results.json must be present with exact content and correct perms."""
    assert PING_RESULTS_FILE.is_file(), f"Missing file: {PING_RESULTS_FILE}"

    perms = _mode(PING_RESULTS_FILE)
    assert perms == 0o644, (
        f"{PING_RESULTS_FILE} should have permissions 644, found {oct(perms)}"
    )

    # Validate JSON content
    with PING_RESULTS_FILE.open() as fp:
        try:
            data = json.load(fp)
        except json.JSONDecodeError as exc:
            pytest.fail(f"{PING_RESULTS_FILE} is not valid JSON: {exc}")  # pragma: no cover

    assert data == EXPECTED_PING_RESULTS, (
        f"{PING_RESULTS_FILE} content differs from expected ground truth."
    )

    # Additional structural sanity checks (redundant but explicit)
    for idx, item in enumerate(data):
        assert set(item) == {"host", "timestamp", "status", "latency_ms"}, (
            f"Element index {idx} in {PING_RESULTS_FILE} does not contain the "
            "required four keys or contains extras."
        )
        assert item["status"] in {"up", "down"}, (
            f"Element index {idx} has invalid status '{item['status']}'."
        )


def test_schema_file_and_permissions():
    """ping_result.schema.json must be present with exact content and correct perms."""
    assert PING_SCHEMA_FILE.is_file(), f"Missing file: {PING_SCHEMA_FILE}"

    perms = _mode(PING_SCHEMA_FILE)
    assert perms == 0o644, (
        f"{PING_SCHEMA_FILE} should have permissions 644, found {oct(perms)}"
    )

    with PING_SCHEMA_FILE.open() as fp:
        try:
            schema = json.load(fp)
        except json.JSONDecodeError as exc:
            pytest.fail(f"{PING_SCHEMA_FILE} is not valid JSON: {exc}")  # pragma: no cover

    assert schema == EXPECTED_PING_SCHEMA, (
        f"{PING_SCHEMA_FILE} content differs from expected ground truth."
    )


def test_computed_uptime_summary_matches_spec():
    """
    Compute uptime statistics from ping_results.json and ensure they match the
    values stated in the task description (db-1 = 100%, web-1 = 75%).
    """
    with PING_RESULTS_FILE.open() as fp:
        data = json.load(fp)

    # Aggregate per host
    stats = {}
    for item in data:
        host = item["host"]
        stats.setdefault(host, {"total": 0, "up": 0})
        stats[host]["total"] += 1
        if item["status"] == "up":
            stats[host]["up"] += 1

    # Expected computed values
    expected = {
        "db-1": {"total": 4, "up": 4, "pct": 100.00},
        "web-1": {"total": 4, "up": 3, "pct": 75.00},
    }

    # Verify host keys
    assert set(stats) == set(expected), (
        f"Hosts present in ping_results.json {set(stats)} "
        f"do not match expected {set(expected)}."
    )

    # Verify each host's counts and calculated percentage
    for host, host_stats in stats.items():
        total = host_stats["total"]
        up = host_stats["up"]
        pct = round((up / total) * 100, 2)

        exp_total = expected[host]["total"]
        exp_up = expected[host]["up"]
        exp_pct = expected[host]["pct"]

        assert total == exp_total, (
            f"{host}: expected total_checks {exp_total}, found {total}"
        )
        assert up == exp_up, (
            f"{host}: expected successful_checks {exp_up}, found {up}"
        )
        assert pct == exp_pct, (
            f"{host}: expected success_rate_percent {exp_pct}, found {pct}"
        )