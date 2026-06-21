# test_initial_state.py
#
# This pytest suite validates that the starting filesystem state is clean
# for the “API availability check” exercise.  Nothing that the student is
# supposed to create later (script, log, CSV) should exist **yet**.
#
# All checks are performed against absolute paths under /home/user.
#
# If any of the assertions below fail, the failure message will clearly
# indicate what file or directory is unexpectedly present or missing.

import os
import stat
import pytest

HOME = "/home/user"

# Paths the student must create later
EXPECTED_SCRIPT_PATH   = os.path.join(HOME, "api_test.sh")
EXPECTED_LOG_PATH      = os.path.join(HOME, "api_test.log")
EXPECTED_SUMMARY_PATH  = os.path.join(HOME, "api_results.csv")

@pytest.fixture(scope="module")
def home_contents():
    """
    Return a set with the names of every entry in /home/user.
    This is used by multiple tests to keep directory listings consistent.
    """
    try:
        return set(os.listdir(HOME))
    except FileNotFoundError:
        # Fail fast – the entire assignment is impossible without /home/user
        pytest.fail(f"Required directory {HOME!r} is missing.",
                    pytrace=False)

def test_home_directory_exists_and_is_directory():
    """Validate that /home/user exists and is a directory."""
    assert os.path.exists(HOME),                f"Directory {HOME!r} is missing."
    assert os.path.isdir(HOME),                 f"{HOME!r} exists but is not a directory."
    # Sanity-check permissions: writable by the current user (octal 0o200)
    mode = os.stat(HOME).st_mode
    assert mode & stat.S_IWUSR,                 f"{HOME!r} is not writable by the current user."

@pytest.mark.parametrize(
    "abs_path,description",
    [
        (EXPECTED_SCRIPT_PATH,  "shell script"),
        (EXPECTED_LOG_PATH,     "log file"),
        (EXPECTED_SUMMARY_PATH, "CSV summary"),
    ],
)
def test_expected_output_paths_do_not_exist_yet(abs_path, description):
    """
    Confirm that none of the artefacts the student is supposed to create
    are already present in the initial filesystem state.
    """
    assert not os.path.exists(abs_path), (
        f"Unexpected {description} found at {abs_path!r}. "
        "The initial environment must not contain any of the files that "
        "the student is expected to create."
    )

def test_no_stray_files_named_like_outputs(home_contents):
    """
    Guard against copy-paste mistakes where extra similarly named files
    might exist (e.g., api_test.sh.txt).
    """
    forbidden_substrings = {"api_test", "api_results"}
    offending = sorted(
        entry for entry in home_contents
        if any(token in entry for token in forbidden_substrings)
        and entry not in {
            os.path.basename(EXPECTED_SCRIPT_PATH),
            os.path.basename(EXPECTED_LOG_PATH),
            os.path.basename(EXPECTED_SUMMARY_PATH),
        }
    )
    assert not offending, (
        "Found unexpected file(s) in /home/user that look related to the "
        f"assignment: {', '.join(offending)}. The starting directory should be clean."
    )