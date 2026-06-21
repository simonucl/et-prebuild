# test_initial_state.py
"""
Pytest suite that verifies the *initial* filesystem/OS state before the
student performs any actions for the “mobile_builder” CI-pipeline task.

Rules verified:
1. /home/user/.ci exists and is a directory.
2. /home/user/.ci/containers_running.txt exists and contains the exact,
   expected “docker ps” snapshot, including:
      • A header line.
      • A data line whose last whitespace-delimited column is the literal
        string “mobile_builder”.
      • That line’s first column is a 12-character CONTAINER ID consisting
        only of [0-9a-f].
      • File ends with a single trailing newline.
3. /home/user/reports does *not* exist yet.
4. /home/user/reports/active_builder.cid does *not* exist yet.
"""

from pathlib import Path
import re
import pytest

HOME = Path("/home/user")
CI_DIR = HOME / ".ci"
CONTAINERS_FILE = CI_DIR / "containers_running.txt"
REPORTS_DIR = HOME / "reports"
CID_FILE = REPORTS_DIR / "active_builder.cid"

MOBILE_BUILDER_ID = "a1b2c3d4e5f6"  # expected ID present in the snapshot


def test_ci_directory_exists_and_is_directory():
    assert CI_DIR.exists(), f"Required directory {CI_DIR} is missing."
    assert CI_DIR.is_dir(), f"{CI_DIR} exists but is not a directory."


def test_containers_file_exists():
    assert CONTAINERS_FILE.exists(), (
        f"Required file {CONTAINERS_FILE} is missing."
    )
    assert CONTAINERS_FILE.is_file(), (
        f"{CONTAINERS_FILE} exists but is not a regular file."
    )


@pytest.fixture(scope="module")
def containers_contents():
    # Read file as bytes to verify trailing newline unambiguously.
    raw = CONTAINERS_FILE.read_bytes()
    return raw


def test_containers_file_trailing_newline(containers_contents):
    assert containers_contents.endswith(b"\n"), (
        f"{CONTAINERS_FILE} must end with exactly one trailing newline."
    )


def test_mobile_builder_row_present_and_correct(containers_contents):
    text = containers_contents.decode("utf-8")
    lines = [ln.rstrip("\n") for ln in text.splitlines()]
    assert len(lines) >= 2, (
        f"{CONTAINERS_FILE} should contain at least a header and "
        f"one data line; found {len(lines)} line(s)."
    )

    # Locate the line whose last whitespace-delimited column is "mobile_builder"
    builder_lines = [
        ln for ln in lines if ln.split() and ln.split()[-1] == "mobile_builder"
    ]
    assert builder_lines, (
        f"No line found in {CONTAINERS_FILE} whose last column "
        f"is the string 'mobile_builder'."
    )
    assert len(builder_lines) == 1, (
        f"Expected exactly one 'mobile_builder' line, found {len(builder_lines)}."
    )

    builder_line = builder_lines[0]
    fields = builder_line.split()
    cid = fields[0]

    assert cid == MOBILE_BUILDER_ID, (
        f"The CONTAINER ID for 'mobile_builder' is expected to be "
        f"'{MOBILE_BUILDER_ID}', but found '{cid}'."
    )

    assert re.fullmatch(r"[0-9a-f]{12}", cid), (
        f"The extracted CONTAINER ID '{cid}' does not match the required "
        f"12-character hex format."
    )


def test_reports_directory_absent():
    assert not REPORTS_DIR.exists(), (
        f"The directory {REPORTS_DIR} should NOT exist before the student "
        f"creates it."
    )


def test_cid_file_absent():
    assert not CID_FILE.exists(), (
        f"The file {CID_FILE} should NOT exist before the student "
        f"creates it."
    )