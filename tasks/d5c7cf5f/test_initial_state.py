# test_initial_state.py
#
# This pytest suite validates that the operating-system / filesystem is still
# in its ORIGINAL state *before* the student starts working on the task.
#
# In other words, none of the required artefacts for the “timezone /
# locale” exercise should exist yet, and the user’s ~/.bashrc must not have
# been modified to source the configuration script.
#
# If any of these tests fail it means the machine is *already* in (or
# partially in) the “final” state, which would invalidate the exercise
# assumptions.

import os
from pathlib import Path
import pytest

HOME = Path("/home/user")
CI_DIR        = HOME / "ci"
CONFIG_DIR    = CI_DIR / "config"
LOGS_DIR      = CI_DIR / "logs"

TZ_LOCALE_SH  = CONFIG_DIR / "timezone_locale.sh"
TIME_LOG      = LOGS_DIR / "time_check.log"
LOCALE_LOG    = LOGS_DIR / "locale_check.log"

BASHRC        = HOME / ".bashrc"
EXPECTED_SRC_LINE = 'source /home/user/ci/config/timezone_locale.sh'


@pytest.mark.parametrize(
    "path_desc, path_obj",
    [
        ("CI root directory", CI_DIR),
        ("config directory",  CONFIG_DIR),
        ("logs directory",    LOGS_DIR),
    ],
)
def test_ci_directories_do_not_exist_yet(path_desc, path_obj):
    """None of the CI-related directories should exist before the task."""
    assert not path_obj.exists(), (
        f"{path_desc} '{path_obj}' already exists. "
        "The exercise assumes a clean slate; please remove it before starting."
    )


@pytest.mark.parametrize(
    "file_desc, file_obj",
    [
        ("configuration script",  TZ_LOCALE_SH),
        ("time verification log", TIME_LOG),
        ("locale verification log", LOCALE_LOG),
    ],
)
def test_ci_files_do_not_exist_yet(file_desc, file_obj):
    """CI configuration / log files must not exist before the task."""
    assert not file_obj.exists(), (
        f"{file_desc} '{file_obj}' already exists. "
        "The exercise requires that you create it as part of your solution."
    )


def test_bashrc_not_modified_yet():
    """
    The very last non-empty line of ~/.bashrc must *not* already source the
    upcoming timezone_locale.sh script.
    """
    if not BASHRC.exists():
        # Nothing to check – a missing ~/.bashrc is fine at this stage.
        return

    try:
        bashrc_content = BASHRC.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        pytest.skip("~/.bashrc contains non-UTF-8 bytes; skipping detailed check.")

    # Strip trailing blank lines to find the last *meaningful* line.
    while bashrc_content and not bashrc_content[-1].strip():
        bashrc_content.pop()

    if not bashrc_content:
        # File is empty – still OK.
        return

    last_line = bashrc_content[-1].rstrip("\n")
    assert last_line != EXPECTED_SRC_LINE, (
        f"~/.bashrc already ends with '{EXPECTED_SRC_LINE}', "
        "but the task instructions state you have to append this line yourself."
    )