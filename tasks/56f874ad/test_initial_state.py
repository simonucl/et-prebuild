# test_initial_state.py
#
# Pytest suite that validates the **initial** filesystem state
# before the student performs any actions for the “project
# re-organisation” task.  It asserts that only the files and
# directories described in the specification are present and that
# key artefacts which must be produced later are **not** present
# yet.  It also validates the exact contents of the supplied log
# files so that later tests can rely on them.

import hashlib
import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path("/home/user/project").resolve()
LOG_DIR = PROJECT_ROOT / "logs"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def sha256_of_file(path: Path) -> str:
    """Return lowercase SHA-256 hex digest of the given file."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_log_line(line: str):
    """
    Parse a semicolon-delimited log line and return tuple:
        (iso_ts, level, node_id, message)
    """
    parts = line.rstrip("\n").split(";", 3)
    if len(parts) != 4:
        raise ValueError(f"Malformed log line: {line!r}")
    return parts  # (timestamp, level, node_id, message)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_project_root_exists_and_is_directory():
    assert PROJECT_ROOT.is_dir(), (
        f"Expected project root directory at {PROJECT_ROOT}, "
        "but it does not exist or is not a directory."
    )


def test_expected_top_level_files_present_and_no_extraneous_dirs():
    """
    Validate that only the expected files exist at the top level and that
    directories that must be created later (`src`, `config`, `scripts`)
    are NOT yet present.
    """
    expected_files = {
        "app.py",
        "helper.py",
        "default.conf",
        "run.sh",
    }
    expected_dirs = {"logs"}

    all_entries = {p.name: p for p in PROJECT_ROOT.iterdir()}

    # Check presence of mandatory files.
    for fname in expected_files:
        path = all_entries.get(fname)
        assert path is not None and path.is_file(), (
            f"Required file {fname!r} is missing from {PROJECT_ROOT}."
        )

    # Check presence of mandatory directory.
    for dname in expected_dirs:
        path = all_entries.get(dname)
        assert path is not None and path.is_dir(), (
            f"Required directory {dname!r} is missing from {PROJECT_ROOT}."
        )

    # Directories that must NOT exist yet.
    forbidden_dirs = {"src", "config", "scripts"}
    for dname in forbidden_dirs:
        path = PROJECT_ROOT / dname
        assert not path.exists(), (
            f"Directory {dname!r} should NOT exist before the re-organisation."
        )

    # Files that must NOT exist yet.
    forbidden_files = {
        "manifest.csv",
        "organize_report.txt",
    }
    for fname in forbidden_files:
        assert not (PROJECT_ROOT / fname).exists(), (
            f"{fname} should NOT exist before the student runs their solution."
        )

    # Summary log file should not exist yet.
    assert not (LOG_DIR / "error_summary.log").exists(), (
        "logs/error_summary.log should NOT exist before log analysis is run."
    )


def test_logs_directory_contains_exact_three_log_files():
    """
    Ensure the `logs` directory exists, contains exactly the three expected
    log files, and nothing else (excluding a future summary file).
    """
    assert LOG_DIR.is_dir(), "logs directory is missing."

    expected_logs = {
        "cluster_node_A.log",
        "cluster_node_B.log",
        "cluster_node_C.log",
    }

    entries = {p.name: p for p in LOG_DIR.iterdir()}

    for fname in expected_logs:
        path = entries.get(fname)
        assert path is not None and path.is_file(), (
            f"Expected log file {fname!r} is missing in {LOG_DIR}."
        )

    # Ensure no unexpected files yet (allow future error_summary.log).
    unexpected = set(entries) - expected_logs
    assert unexpected <= {"error_summary.log"}, (
        f"Unexpected files present in logs directory: {unexpected}"
    )


@pytest.mark.parametrize(
    "log_filename, expected_counts",
    [
        ("cluster_node_A.log", {"NodeA": {"ERROR": 2, "WARN": 1}}),
        ("cluster_node_B.log", {"NodeB": {"ERROR": 1, "WARN": 2}}),
        ("cluster_node_C.log", {"NodeC": {"ERROR": 0, "WARN": 1}}),
    ],
)
def test_each_log_file_contains_expected_counts(log_filename, expected_counts):
    """
    Parse each individual log file and verify the ERROR/WARN counts for
    its single node.
    """
    log_path = LOG_DIR / log_filename
    assert log_path.is_file(), f"Log file {log_filename} is missing."

    # Initialize counters
    counters = {node: {"ERROR": 0, "WARN": 0} for node in expected_counts}

    with log_path.open("r", encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            ts, level, node_id, _msg = parse_log_line(line)

            # basic ISO-8601 date/time sanity check
            iso_pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
            assert re.match(iso_pattern, ts), (
                f"Line {lineno} in {log_filename} has invalid timestamp {ts!r}"
            )

            if node_id in counters and level in counters[node_id]:
                counters[node_id][level] += 1

    # Assert counts match expectation
    for node, counts in expected_counts.items():
        for lvl, expected_value in counts.items():
            assert counters[node][lvl] == expected_value, (
                f"{log_filename}: expected {expected_value} {lvl} lines for "
                f"{node}, found {counters[node][lvl]}"
            )


def test_overall_log_counts_across_files():
    """
    Aggregate all *.log files and cross-validate that the combined counts
    match the specification.  This guards against duplication or missing
    lines across files.
    """
    expected_overall = {
        "NodeA": {"ERROR": 2, "WARN": 1},
        "NodeB": {"ERROR": 1, "WARN": 2},
        "NodeC": {"ERROR": 0, "WARN": 1},
    }

    totals = {n: {"ERROR": 0, "WARN": 0} for n in expected_overall}

    for log_file in LOG_DIR.glob("*.log"):
        # Skip summary file if it somehow exists (already checked earlier)
        if log_file.name == "error_summary.log":
            continue
        with log_file.open("r", encoding="utf-8") as fh:
            for line in fh:
                _ts, level, node_id, _msg = parse_log_line(line)
                if node_id in totals and level in totals[node_id]:
                    totals[node_id][level] += 1

    for node, counts in expected_overall.items():
        for lvl, expected_val in counts.items():
            assert totals[node][lvl] == expected_val, (
                f"Across all logs, expected {expected_val} {lvl} for {node}, "
                f"got {totals[node][lvl]}"
            )