# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem *before*
# the student performs any actions on the terminal.  It asserts the exact
# initial conditions described in the task narrative so that subsequent
# grading can rely on a known-good starting point.
#
# The checks performed:
#   1. Required directories exist (uptime_monitor/ and uptime_monitor/reports/).
#   2. The reports directory contains *exactly* two files:
#        • uptime_2024-04-25.log         (empty file, size == 0)
#        • uptime_2024-04-25.log.sha256  (contains the canonical SHA-256 line)
#   3. The manifest’s contents match the SHA-256 digest of the empty report.
#   4. No “verification” directory (or its log file) exists yet.
#
# Only stdlib + pytest are used.

import hashlib
from pathlib import Path

import pytest

HOME = Path("/home/user")
ROOT_DIR = HOME / "uptime_monitor"
REPORTS_DIR = ROOT_DIR / "reports"

REPORT_FILE = REPORTS_DIR / "uptime_2024-04-25.log"
MANIFEST_FILE = REPORTS_DIR / "uptime_2024-04-25.log.sha256"

VERIFICATION_DIR = ROOT_DIR / "verification"
VERIFICATION_LOG = VERIFICATION_DIR / "sha256_check.log"

EXPECTED_DIGEST = (
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
)  # sha256 of empty file
EXPECTED_MANIFEST_LINE = (
    f"{EXPECTED_DIGEST}  uptime_2024-04-25.log\n"
)  # two spaces before filename + trailing \n


@pytest.mark.order(1)
def test_required_directories_exist():
    """Ensure /home/user/uptime_monitor/reports exists."""
    assert ROOT_DIR.is_dir(), (
        "Missing directory: "
        f"{ROOT_DIR}.  The base directory for uptime_monitor must exist."
    )
    assert REPORTS_DIR.is_dir(), (
        "Missing directory: "
        f"{REPORTS_DIR}.  The 'reports' directory must exist before any action."
    )


@pytest.mark.order(2)
def test_reports_directory_contains_only_expected_files():
    """The reports directory should have exactly the two expected files."""
    expected_names = {REPORT_FILE.name, MANIFEST_FILE.name}
    actual_names = {p.name for p in REPORTS_DIR.iterdir()}
    assert actual_names == expected_names, (
        f"{REPORTS_DIR} should contain only {sorted(expected_names)}, "
        f"but found {sorted(actual_names)}"
    )


@pytest.mark.order(3)
def test_report_file_is_empty():
    """The report file must exist and be zero bytes."""
    assert REPORT_FILE.is_file(), f"Missing report file: {REPORT_FILE}"
    size = REPORT_FILE.stat().st_size
    assert size == 0, f"{REPORT_FILE} should be empty (0 bytes) but is {size} bytes"


@pytest.mark.order(4)
def test_manifest_file_contents_and_checksum():
    """Verify manifest content matches the known SHA-256 of the empty report."""
    assert MANIFEST_FILE.is_file(), f"Missing manifest file: {MANIFEST_FILE}"

    # Read manifest bytes exactly as-is.
    manifest_bytes = MANIFEST_FILE.read_bytes()
    expected_bytes = EXPECTED_MANIFEST_LINE.encode("utf-8")
    assert (
        manifest_bytes == expected_bytes
    ), "Manifest file contents do not match the expected canonical line"

    # Independently compute the digest of the report file and compare.
    digest = hashlib.sha256(REPORT_FILE.read_bytes()).hexdigest()
    assert (
        digest == EXPECTED_DIGEST
    ), f"Computed SHA-256 digest {digest} does not match expected {EXPECTED_DIGEST}"


@pytest.mark.order(5)
def test_verification_directory_absent():
    """
    Before the student runs any commands the verification directory
    and its log file must *not* exist.
    """
    assert not VERIFICATION_DIR.exists(), (
        f"Directory {VERIFICATION_DIR} should not exist before verification begins."
    )
    # If the directory were present, the log could still be missing, so guard that too.
    assert not VERIFICATION_LOG.exists(), (
        f"Log file {VERIFICATION_LOG} should not exist before verification begins."
    )