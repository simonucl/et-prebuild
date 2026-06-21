# test_initial_state.py
#
# This pytest suite verifies the *initial* state of the operating-system /
# file-system for the “active users” exercise *before* the student performs
# any actions.
#
# It asserts that:
#   • /home/user/project/data/users.csv exists and contains the expected
#     five lines (header + 4 data rows) exactly.
#   • The yet-to-be-created artefacts
#         /home/user/project/data/active_users.csv
#         /home/user/project/data/active_users.json
#         /home/user/project/logs/process.log
#     do **not** exist.
#
# All messages have been written to be as explicit and helpful as possible if
# any assertion fails.
#
# NOTE: Only stdlib + pytest are used, per rubric.

from pathlib import Path
import pytest

HOME = Path("/home/user")
PROJECT_DIR = HOME / "project"
DATA_DIR = PROJECT_DIR / "data"
LOGS_DIR = PROJECT_DIR / "logs"

USERS_CSV = DATA_DIR / "users.csv"
ACTIVE_USERS_CSV = DATA_DIR / "active_users.csv"
ACTIVE_USERS_JSON = DATA_DIR / "active_users.json"
PROCESS_LOG = LOGS_DIR / "process.log"


# --------------------------------------------------------------------------- #
# Helpers                                                                     #
# --------------------------------------------------------------------------- #
@pytest.fixture(scope="module")
def expected_users_csv_lines():
    """
    The exact lines (including commas and order of columns) that must be
    present in /home/user/project/data/users.csv at the start of the exercise.
    Each line *ends* with a newline character in the canonical form, but when
    we compare we strip trailing newlines to be tolerant of final newline
    presence/absence.
    """
    return [
        "id,name,email,status",
        "1,John Doe,john@example.com,active",
        "2,Jane Smith,jane@sample.com,inactive",
        "3,Bob Lee,bob@domain.com,active",
        "4,Alice Kay,alice@website.org,pending",
    ]


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #
def test_users_csv_exists(expected_users_csv_lines):
    """
    Ensure the input CSV file exists at the correct absolute path and contains
    precisely the five expected lines.
    """
    assert USERS_CSV.exists(), (
        f"Required file not found: {USERS_CSV}.\n"
        "Make sure the sample data-set is present at the expected location."
    )

    assert USERS_CSV.is_file(), f"Expected {USERS_CSV} to be a file, not a directory."

    actual_lines = USERS_CSV.read_text(encoding="utf-8").splitlines()

    # Compare number of lines first for a clearer message.
    expected_count = len(expected_users_csv_lines)
    actual_count = len(actual_lines)
    assert (
        actual_count == expected_count
    ), f"{USERS_CSV} should have {expected_count} lines (header + 4 rows), but has {actual_count}."

    # Compare each line ignoring trailing newline differences.
    mismatches = [
        (idx + 1, exp, act)
        for idx, (exp, act) in enumerate(zip(expected_users_csv_lines, actual_lines))
        if exp != act
    ]
    assert not mismatches, (
        f"Content mismatch in {USERS_CSV}:\n"
        + "\n".join(
            f"  line {ln}: expected '{exp}' but found '{act}'" for ln, exp, act in mismatches
        )
    )


@pytest.mark.parametrize(
    "path_under_test",
    [ACTIVE_USERS_CSV, ACTIVE_USERS_JSON, PROCESS_LOG],
)
def test_output_files_do_not_yet_exist(path_under_test):
    """
    The exercise instructs the student to create these artefacts. At the initial
    state they must *not* be present.
    """
    assert (
        not path_under_test.exists()
    ), f"{path_under_test} should NOT exist before the student runs their code."