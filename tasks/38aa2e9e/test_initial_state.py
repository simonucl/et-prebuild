# test_initial_state.py
#
# Pytest suite that verifies the _starting_ filesystem state for the
# “Generate lint-clean Markdown from an Nmap .gnmap file” exercise.
#
# The tests assert that:
#   • The seed directory /home/user/scan-results exists.
#   • The seed file /home/user/scan-results/nmap_output.gnmap exists
#     and its contents match exactly what the assignment specifies.
#   • Neither /home/user/scan-results/OpenPorts.md nor
#     /home/user/scan-results/lint_report.log exists yet.
#
# These checks guarantee that the student begins from the expected
# environment and that the grader can rely on a clean slate.

import os
from pathlib import Path

import pytest


SCAN_DIR = Path("/home/user/scan-results")
GNMAP_FILE = SCAN_DIR / "nmap_output.gnmap"
MARKDOWN_FILE = SCAN_DIR / "OpenPorts.md"
LINT_FILE = SCAN_DIR / "lint_report.log"

# Exact canonical content (including newlines) that must already be
# present in nmap_output.gnmap before any student command runs.
EXPECTED_GNMAP_CONTENT = (
    "# Nmap 7.80 scan initiated\n"
    "Host: 10.10.0.5 ()  Status: Up\n"
    "Host: 10.10.0.5 ()  Ports: 21/open/tcp//ftp///, 80/open/tcp//http///, 8080/open/tcp//http-proxy///\n"
    "Host: 10.10.0.15 () Status: Up\n"
    "Host: 10.10.0.15 () Ports: 22/open/tcp//ssh///, 139/open/tcp//netbios-ssn///, 445/open/tcp//microsoft-ds///\n"
    "# Nmap done\n"
)


def test_scan_directory_exists():
    """Verify that /home/user/scan-results exists and is a directory."""
    assert SCAN_DIR.exists(), f"Required directory missing: {SCAN_DIR}"
    assert SCAN_DIR.is_dir(), f"Expected {SCAN_DIR} to be a directory."


def test_gnmap_file_exists_with_expected_content_and_permissions():
    """
    The seed .gnmap file must exist, be a regular file, readable by the
    current user, and contain exactly the predefined text.
    """
    assert GNMAP_FILE.exists(), f"Seed file missing: {GNMAP_FILE}"
    assert GNMAP_FILE.is_file(), f"{GNMAP_FILE} is not a regular file."

    # Permissions: world‐readable OK, but user must be able to read/write.
    stat = GNMAP_FILE.stat()
    # Owner write bit should be set (0o200).
    assert stat.st_mode & 0o200, (
        f"{GNMAP_FILE} should be writable by the owner (mode 0644 recommended)."
    )

    # Read entire file as text and compare verbatim.
    content = GNMAP_FILE.read_text(encoding="utf-8")
    assert (
        content == EXPECTED_GNMAP_CONTENT
    ), "Contents of nmap_output.gnmap do not match the expected baseline."


@pytest.mark.parametrize(
    "path,label",
    [
        (MARKDOWN_FILE, "OpenPorts.md"),
        (LINT_FILE, "lint_report.log"),
    ],
)
def test_output_files_do_not_exist_yet(path: Path, label: str):
    """
    Before the student runs their command, the output artefacts must NOT
    exist.  Their presence would indicate that the environment is dirty
    or that a previous run polluted the workspace.
    """
    assert not path.exists(), (
        f"{label} already exists at {path}. The workspace must start clean."
    )