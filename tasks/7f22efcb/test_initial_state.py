# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the on-disk fixture
# before the student starts working.  It asserts the exact directory tree,
# the exact contents of every .trace file (all lowercase “timeout”, no
# uppercase “TIMEOUT”), and the absence of any artefacts that the student
# is expected to create later.

import os
from pathlib import Path

ROOT      = Path("/home/user")
LOGS_ROOT = ROOT / "network_logs"
AUDIT_DIR = ROOT / "network_audit"

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def count_token(text: str, token: str) -> int:
    """Return the number of (non-overlapping) occurrences of *token* in text."""
    return text.count(token)


# --------------------------------------------------------------------------- #
# Ground-truth for the initial fixture
# --------------------------------------------------------------------------- #
EXPECTED_TRACE_FILES = {
    LOGS_ROOT / "region1" / "router1.trace": (
        "PING 10.0.0.1\n"
        "success\n"
        "timeout\n"
        "timeout\n"
        "timeout\n"
        "end\n"
    ),
    LOGS_ROOT / "region1" / "router2.trace": (
        "PING 10.0.0.2\n"
        "success\n"
        "end\n"
    ),
    LOGS_ROOT / "region2" / "router3.trace": (
        "TRACE 10.1.0.1\n"
        "timeout\n"
        "ok\n"
        "timeout\n"
        "end\n"
    ),
    LOGS_ROOT / "region2" / "backup" / "router4.trace": (
        "PROBE 10.2.0.1\n"
        "timeout\n"
        "timeout\n"
        "timeout\n"
        "timeout\n"
        "timeout\n"
        "done\n"
    ),
}

# Pre-calculated expected counts of lowercase “timeout”
EXPECTED_TIMEOUT_COUNTS = {
    path: content.count("timeout")  # counts are 3, 0, 2, 5 respectively
    for path, content in EXPECTED_TRACE_FILES.items()
}


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_directory_structure_exists():
    """
    Verify that /home/user/network_logs and all expected sub-directories exist.
    """
    assert LOGS_ROOT.is_dir(), f"Missing directory: {LOGS_ROOT}"
    for file_path in EXPECTED_TRACE_FILES:
        assert file_path.parent.is_dir(), f"Missing directory: {file_path.parent}"


def test_exactly_four_trace_files_present():
    """
    There must be exactly the four expected *.trace* files under
    /home/user/network_logs.
    """
    found = {p for p in LOGS_ROOT.rglob("*.trace")}
    expected = set(EXPECTED_TRACE_FILES.keys())
    assert found == expected, (
        "The set of .trace files on disk does not match the expected set.\n"
        f"Expected ({len(expected)}):\n  " + "\n  ".join(map(str, sorted(expected))) +
        f"\nFound ({len(found)}):\n  " + "\n  ".join(map(str, sorted(found)))
    )


def test_trace_file_contents_and_timeout_counts():
    """
    Each .trace file must exactly match the expected contents:
      • Lower-case 'timeout' tokens appear in the expected number.
      • No upper-case 'TIMEOUT' tokens are present yet.
    """
    for path, expected_content in EXPECTED_TRACE_FILES.items():
        assert path.is_file(), f"Missing .trace file: {path}"

        actual = path.read_text(encoding="utf-8")
        assert actual == expected_content, (
            f"Contents of {path} differ from the expected fixture."
        )

        lower = count_token(actual, "timeout")
        upper = count_token(actual, "TIMEOUT")
        assert lower == EXPECTED_TIMEOUT_COUNTS[path], (
            f"{path} should contain {EXPECTED_TIMEOUT_COUNTS[path]} "
            f"lower-case 'timeout' tokens but has {lower}."
        )
        assert upper == 0, f"{path} should not contain any upper-case 'TIMEOUT' tokens yet."


def test_no_count_files_exist_initially():
    """
    The *.trace.count files must NOT exist before the student runs their commands.
    """
    count_files = list(LOGS_ROOT.rglob("*.trace.count"))
    assert not count_files, (
        "Found .count files before the student started:\n  "
        + "\n  ".join(map(str, count_files))
    )


def test_audit_directory_absent_initially():
    """
    /home/user/network_audit/ and connectivity_report.log must not exist yet.
    """
    assert not AUDIT_DIR.exists(), (
        f"{AUDIT_DIR} should not exist before the student creates it."
    )