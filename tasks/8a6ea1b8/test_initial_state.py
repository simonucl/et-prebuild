# test_initial_state.py
#
# This test-suite validates that the operating-system / filesystem is in the
# expected “pre-task” state *before* the student performs any action.
#
# What we expect *before* the task starts:
#
# 1.  /home/user/raw_data/measurements.txt
#       • Must exist.
#       • Must contain exactly the five data rows plus header shown in the
#         assignment (including the single trailing newline).
#
# 2.  /home/user/opt_solver
#       • May or may not exist, but none of the three artefacts that the
#         student is supposed to create (input_data.csv, config.json,
#         prep_summary.log) are allowed to exist yet.  Their presence would
#         indicate that the workspace is “dirty” and therefore invalid for
#         the exercise.
#
# Only stdlib + pytest are used.

from pathlib import Path
import pytest

# --------------------------------------------------------------------------------------
# CONSTANTS
# --------------------------------------------------------------------------------------

RAW_FILE = Path("/home/user/raw_data/measurements.txt")
OPT_SOLVER_DIR = Path("/home/user/opt_solver")
OUTPUT_FILES = {
    "input_csv": OPT_SOLVER_DIR / "input_data.csv",
    "config_json": OPT_SOLVER_DIR / "config.json",
    "prep_log": OPT_SOLVER_DIR / "prep_summary.log",
}

EXPECTED_MEASUREMENTS_CONTENT = (
    "ID F1 F2 target\n"
    "1 3.5 7.2 10.7\n"
    "2 NaN 6.1 8.2\n"
    "3 4.1 5.9 10.0\n"
    "4 3.9 NaN 9.5\n"
    "5 4.2 6.5 10.7\n"
)

# --------------------------------------------------------------------------------------
# TESTS
# --------------------------------------------------------------------------------------


def test_raw_measurements_file_exists():
    """The raw measurements file must be present."""
    assert RAW_FILE.exists(), (
        f"Missing required raw data file: {RAW_FILE}. "
        "The initial dataset must be provided before the task begins."
    )
    assert RAW_FILE.is_file(), f"{RAW_FILE} exists but is not a regular file."


def test_raw_measurements_file_contents():
    """The raw measurements file must match the expected reference content exactly."""
    content = RAW_FILE.read_text(encoding="utf-8")
    assert (
        content == EXPECTED_MEASUREMENTS_CONTENT
    ), (
        "The contents of /home/user/raw_data/measurements.txt do not match the expected "
        "initial dataset. Make sure the file has exactly the five rows plus header, "
        "whitespace, and a single final newline as specified.\n\n"
        "Expected:\n"
        f"{EXPECTED_MEASUREMENTS_CONTENT!r}\n\nGot:\n{content!r}"
    )


@pytest.mark.parametrize("file_key", list(OUTPUT_FILES.keys()))
def test_output_files_do_not_exist_yet(file_key):
    """
    Before the student starts, none of the target output artefacts are allowed
    to exist.  Their existence would mean the environment is not in a clean
    initial state, which could hide mistakes or break the evaluation.
    """
    path = OUTPUT_FILES[file_key]
    assert (
        not path.exists()
    ), (
        f"Pre-existing file {path} detected. The workspace must be clean before the task "
        "starts; remove this file so the student can generate it during the exercise."
    )