# test_initial_state.py
#
# This test-suite makes sure the working environment is **clean**
# before the student starts creating the required time-zone showcase.
# Nothing from the expected end-state must be present yet.

import os
import pytest

HOME = "/home/user"
BASE_DIR = os.path.join(HOME, "techdocs")
TARGET_DIR = os.path.join(BASE_DIR, "timezone_locale")
CONFIG_INI = os.path.join(TARGET_DIR, "config.ini")
SAMPLE_LOG = os.path.join(TARGET_DIR, "sample_times.log")


@pytest.mark.parametrize(
    "path, kind",
    [
        (TARGET_DIR, "directory"),
        (CONFIG_INI, "file"),
        (SAMPLE_LOG, "file"),
    ],
)
def test_expected_artifacts_do_not_exist_yet(path, kind):
    """
    Before the student performs any action, none of the final artifacts
    may be present.  A pre-existing file or directory would indicate that
    the starting snapshot is dirty and would invalidate the exercise.
    """
    assert not os.path.exists(
        path
    ), (
        f"The expected {kind} '{path}' already exists. "
        "The workspace must start in a clean state."
    )