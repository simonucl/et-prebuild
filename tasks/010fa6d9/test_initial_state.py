# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem **before**
# the student begins work on ticket #5502.
#
# It checks that:
#   • The cluster_status directory exists.
#   • Exactly the three expected *.status files are present.
#   • Each file contains the correct two-line key/value pairs.
#   • node-beta is the only node reporting STATE=FAIL.
#   • The resolution log does NOT yet exist.
#
# Any failure clearly explains what is missing or wrong.

import pathlib
import pytest

HOME = pathlib.Path("/home/user").expanduser()
TICKET_DIR = HOME / "tickets" / "ticket-5502"
STATUS_DIR = TICKET_DIR / "cluster_status"

EXPECTED_STATUS = {
    "node-alpha.status": "OK",
    "node-beta.status": "FAIL",
    "node-gamma.status": "OK",
}

RESOLUTION_LOG = TICKET_DIR / "resolution.log"


def read_file(path: pathlib.Path) -> list[str]:
    """Read a text file and return a list of stripped lines."""
    return path.read_text(encoding="utf-8").splitlines()


def test_cluster_status_directory_exists():
    assert STATUS_DIR.exists(), (
        f"Expected directory {STATUS_DIR} to exist, but it is missing."
    )
    assert STATUS_DIR.is_dir(), (
        f"Expected {STATUS_DIR} to be a directory, but it is not."
    )


def test_expected_status_files_present_and_no_extras():
    present_files = sorted(p.name for p in STATUS_DIR.glob("*.status"))
    expected_files = sorted(EXPECTED_STATUS.keys())
    assert present_files == expected_files, (
        "Mismatch in *.status files.\n"
        f"Expected exactly: {expected_files}\n"
        f"Found instead:    {present_files}"
    )


@pytest.mark.parametrize("filename,expected_state", EXPECTED_STATUS.items())
def test_each_status_file_contents(filename, expected_state):
    path = STATUS_DIR / filename
    assert path.exists(), f"File {path} is missing."
    assert path.is_file(), f"{path} should be a regular file."

    lines = read_file(path)
    assert len(lines) == 2, (
        f"{path} should contain exactly 2 lines (SERVICE and STATE) "
        f"but contains {len(lines)} line(s)."
    )

    service_line, state_line = lines
    assert service_line == "SERVICE=db", (
        f"{path}: First line should be 'SERVICE=db' but is '{service_line}'."
    )
    assert state_line.startswith("STATE="), (
        f"{path}: Second line should start with 'STATE=' but is '{state_line}'."
    )
    actual_state = state_line.split("=", 1)[1]
    assert actual_state == expected_state, (
        f"{path}: Expected STATE={expected_state} but found STATE={actual_state}."
    )


def test_resolution_log_not_yet_present():
    assert not RESOLUTION_LOG.exists(), (
        f"{RESOLUTION_LOG} should NOT exist before the student starts.\n"
        f"Delete it or rename it so the student can create it afresh."
    )