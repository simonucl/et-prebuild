# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem state
# before the student performs any actions for the “hostname
# migration” exercise.
#
# The assertions here must all PASS on the pristine system and
# should FAIL once the student has carried out the required
# migration steps.  Clear assertion messages are provided so
# that any deviation from the expected starting conditions is
# immediately obvious.

import json
from pathlib import Path

import pytest

HOME = Path("/home/user")
PROJECT_ROOT = HOME / "projects" / "microservices"

# ---------------------------------------------------------------------------
# Helper data structures describing the expected initial state
# ---------------------------------------------------------------------------

# Mapping: absolute file path  ->  list of expected *full* lines (no \n)
CONF_EXPECTED_LINES = {
    PROJECT_ROOT / "serviceA" / "config" / "app.conf": [
        "DB_HOST=legacy.internal.example.com",
        "CACHE_HOST=legacy.internal.example.com",
    ],
    PROJECT_ROOT / "serviceA" / "config" / "db.conf": [
        "jdbc=postgres://legacy.internal.example.com:5432/prod",
    ],
    PROJECT_ROOT / "serviceB" / "config" / "web.conf": [
        "upstream legacy.internal.example.com;",
    ],
    PROJECT_ROOT / "serviceB" / "config" / "cache.conf": [
        "cache_server=legacy.internal.example.com",
        "metrics_host=legacy.internal.example.com",
        "backup_host=legacy.internal.example.com",
    ],
    PROJECT_ROOT / "serviceC" / "config" / "worker.conf": [
        "queue=amqp://legacy.internal.example.com",
    ],
}

# Expected *.sh files that must already exist
SCRIPT_PATHS = [
    PROJECT_ROOT / "serviceA" / "scripts" / "deploy.sh",
    PROJECT_ROOT / "serviceB" / "scripts" / "restart.sh",
    PROJECT_ROOT / "serviceC" / "scripts" / "cleanup.sh",
]

# Paths that must *not* exist in the initial state
MISSING_PATHS = [
    HOME / "migration_logs",
    HOME / "migration_backup",
    HOME / "migration_logs" / "hostname_migration.log",
]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("conf_path,expected_lines", CONF_EXPECTED_LINES.items())
def test_conf_files_exist_with_legacy_hostname(conf_path: Path, expected_lines):
    """
    Each *.conf file must exist with the exact expected lines that still
    reference the legacy hostname.  There must be NO occurrence of the
    new hostname at this stage.
    """
    assert conf_path.is_file(), f"Missing config file: {conf_path!s}"

    with conf_path.open(encoding="utf-8") as fh:
        file_lines = [ln.rstrip("\n") for ln in fh.readlines()]

    # Exact content match (order & count)
    assert (
        file_lines == expected_lines
    ), f"Unexpected content for {conf_path}. Expected lines:\n{expected_lines}\nFound lines:\n{file_lines}"

    # Confirm absence of the replacement hostname
    bad_lines = [ln for ln in file_lines if "cloud.internal.example.com" in ln]
    assert (
        not bad_lines
    ), f"{conf_path} should not yet contain 'cloud.internal.example.com' but it does in lines: {bad_lines}"


def test_total_legacy_occurrences():
    """
    Sanity-check: across all *.conf files there should be exactly eight
    occurrences of the legacy hostname.
    """
    total = 0
    for conf_path in CONF_EXPECTED_LINES:
        text = conf_path.read_text(encoding="utf-8")
        total += text.count("legacy.internal.example.com")
    assert (
        total == 8
    ), f"Expected exactly 8 occurrences of legacy hostname across all .conf files, found {total}"


@pytest.mark.parametrize("script_path", SCRIPT_PATHS)
def test_helper_scripts_exist(script_path: Path):
    """
    All helper *.sh scripts referenced in the task description must already
    exist.  We intentionally do NOT validate their mtime here—only presence.
    """
    assert script_path.is_file(), f"Missing script: {script_path!s}"


@pytest.mark.parametrize("abs_path", MISSING_PATHS)
def test_migration_directories_and_log_do_not_exist_yet(abs_path: Path):
    """
    Neither the migration_logs directory nor the migration_backup directory
    (nor the log file itself) should be present yet.
    """
    assert not abs_path.exists(), f"{abs_path} should NOT exist before migration starts"


def test_no_json_log_lines_present_yet(tmp_path):
    """
    Ensure that no stray hostname_migration.log file is hiding elsewhere in
    the filesystem tree at this point.  A quick walk from /home/user is
    sufficient and avoids probing outside the allowed area.
    """
    suspected = list(HOME.rglob("hostname_migration.log"))
    assert (
        not suspected
    ), f"Found unexpected hostname_migration.log files: {suspected}"


def test_conf_files_contain_valid_utf8():
    """
    Guard against corrupted encodings that would break later processing.
    """
    for conf_path in CONF_EXPECTED_LINES:
        try:
            conf_path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            pytest.fail(f"{conf_path} is not valid UTF-8: {exc}")