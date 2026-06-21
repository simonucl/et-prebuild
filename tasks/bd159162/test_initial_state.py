# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state before the learner performs any actions for the “ticket frequency
# report” task.  It checks that the expected source directory and log files
# are present and that their exact contents match the ground truth provided
# in the assignment description.
#
# NOTE:  Per the grading guidelines we intentionally do *not* test for the
#        presence (or absence) of any output artefacts such as
#        “issue_summary.txt” – only the initial inputs.

from pathlib import Path
from collections import Counter
import pytest

# ---------------------------------------------------------------------------
# Canonical paths & canonical file contents (including trailing '\n')
# ---------------------------------------------------------------------------

TICKETS_DIR = Path("/home/user/tickets")

EXPECTED_CONTENT_2023_10_01 = (
    "TCKT-1001, alice, NET-001\n"
    "TCKT-1002, bob, PRN-404\n"
    "TCKT-1003, carol, NET-001\n"
    "TCKT-1004, dave, SEC-900\n"
    "TCKT-1005, erin, NET-001\n"
    "TCKT-1006, frank, PRN-404\n"
)

EXPECTED_CONTENT_2023_10_02 = (
    "TCKT-1007, george, SEC-900\n"
    "TCKT-1008, hannah, SEC-900\n"
    "TCKT-1009, ian, NET-001\n"
    "TCKT-1010, jane, PRN-404\n"
    "TCKT-1011, kevin, NET-001\n"
    "TCKT-1012, laura, PRN-404\n"
    "TCKT-1013, mike, NET-001\n"
    "TCKT-1014, nancy, NET-001\n"
)

# Mapping: filename -> expected text
EXPECTED_LOGS = {
    "2023-10-01.log": EXPECTED_CONTENT_2023_10_01,
    "2023-10-02.log": EXPECTED_CONTENT_2023_10_02,
}

# Ground-truth ISSUE_CODE frequency counts derived from the two logs
EXPECTED_COUNTS = {
    "NET-001": 7,
    "PRN-404": 4,
    "SEC-900": 3,
}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_tickets_directory_exists_and_is_dir():
    """
    /home/user/tickets must exist and be a directory.  The remainder of the
    tests rely on this path being correct.
    """
    assert TICKETS_DIR.exists(), (
        "Directory '/home/user/tickets' is missing.  The two source log "
        "files must live in this directory."
    )
    assert TICKETS_DIR.is_dir(), (
        "'/home/user/tickets' exists but is *not* a directory."
    )


@pytest.mark.parametrize("filename,expected_text", EXPECTED_LOGS.items())
def test_each_log_file_exists_and_matches_expected_contents(filename, expected_text):
    """
    Verify that each required log file is present and *exactly* matches the
    canonical content (including the trailing newline).
    """
    path = TICKETS_DIR / filename

    assert path.exists(), f"Required log file '{path}' is missing."
    assert path.is_file(), f"'{path}' exists but is not a regular file."

    actual_text = path.read_text(encoding="utf-8")
    assert actual_text == expected_text, (
        f"Contents of '{path}' differ from the expected ground truth.  Make "
        "sure the file has not been modified and that it ends with a newline."
    )


def test_issue_code_frequencies_match_ground_truth():
    """
    Parse the two expected log texts and confirm that the ISSUE_CODE
    frequencies match the ground-truth counts provided in the assignment.
    """
    counts = Counter()

    for expected_text in EXPECTED_LOGS.values():
        for line in expected_text.splitlines():
            # Each line is of the form:  TICKET_ID, USERNAME, ISSUE_CODE
            parts = line.split(",", maxsplit=2)
            assert len(parts) == 3, (
                "Log line does not have exactly three comma-separated fields: "
                f'{line!r}'
            )
            issue_code = parts[2].strip()
            counts[issue_code] += 1

    assert counts == EXPECTED_COUNTS, (
        "Computed ISSUE_CODE frequencies do not match the ground truth.\n"
        f"Expected: {EXPECTED_COUNTS}\n"
        f"Found:    {dict(counts)}"
    )