# test_initial_state.py
#
# This test-suite verifies that the operating-system / filesystem
# is still in its ORIGINAL, unmodified state **before** the student
# starts working on the “server_configs” task.  All checks assert
# that none of the deliverables required by the assignment are
# present yet and that no side-effects have accidentally been
# applied to the user’s environment.
#
# If any test in this file fails it means the starting snapshot is
# already “dirty” and the student would not be able to complete the
# assignment under clean-room conditions.

import os
import stat
from pathlib import Path

HOME = Path("/home/user")
SERVER_CONFIGS = HOME / "server_configs"

# Individual paths the assignment is supposed to create **later**
TIME_SETTINGS_DIR   = SERVER_CONFIGS / "time_settings"
LOCALE_SETTINGS_DIR = SERVER_CONFIGS / "locale_settings"

TIMEZONE_TXT  = TIME_SETTINGS_DIR   / "timezone.txt"
LOCALE_GEN    = LOCALE_SETTINGS_DIR / "locale.gen"
LOCALE_CONF   = LOCALE_SETTINGS_DIR / "locale.conf"
APPLY_SCRIPT  = SERVER_CONFIGS      / "apply_settings.sh"
APPLY_LOG     = SERVER_CONFIGS      / "apply_settings.log"

USER_TIMEZONE = HOME / ".timezone"
USER_BASHRC   = HOME / ".bashrc"

LOCALE_LINES = [
    "LANG=en_US.UTF-8",
    "LC_CTYPE=en_US.UTF-8",
    "LC_TIME=de_DE.UTF-8",
    "LC_NUMERIC=en_US.UTF-8",
    "LC_MONETARY=en_US.UTF-8",
]


def _nice_path(path: Path) -> str:
    """Return a printable, absolute path string."""
    return str(path.resolve())


def test_server_configs_not_present_yet():
    """
    The top-level directory 'server_configs' (and therefore everything
    below it) should NOT exist before the student starts the task.
    """
    assert not SERVER_CONFIGS.exists(), (
        f"The directory {_nice_path(SERVER_CONFIGS)} should NOT exist yet. "
        "The workspace must begin in a pristine state."
    )


def test_individual_deliverables_absent():
    """
    None of the deliverable files or sub-directories should be present.
    This includes time-zone and locale files, the shell script and the log.
    """
    for path in [
        TIME_SETTINGS_DIR,
        LOCALE_SETTINGS_DIR,
        TIMEZONE_TXT,
        LOCALE_GEN,
        LOCALE_CONF,
        APPLY_SCRIPT,
        APPLY_LOG,
    ]:
        assert not path.exists(), (
            f"Unexpected pre-existing file or directory: {_nice_path(path)}. "
            "The assignment must start with NO deliverables in place."
        )


def test_no_timezone_file_in_home():
    """
    The assignment’s shell script is supposed to create ~/.timezone.
    It must therefore not exist at this point.
    """
    assert not USER_TIMEZONE.exists(), (
        f"Found pre-existing file {_nice_path(USER_TIMEZONE)}. "
        "The .timezone file should only appear AFTER the student runs "
        "their apply_settings.sh script."
    )


def test_bashrc_is_clean_of_locale_lines():
    """
    If ~/.bashrc already exists (many base images provide one), it should
    *not* yet contain any of the five locale assignments the student is
    asked to append.  If the file does not exist, that is also fine.
    """
    if not USER_BASHRC.exists():
        # Nothing to check; the file will be created or updated later.
        return

    try:
        bashrc_content = USER_BASHRC.read_text(encoding="utf-8", errors="ignore").splitlines()
    except Exception as exc:
        raise AssertionError(
            f"Could not read {_nice_path(USER_BASHRC)} while verifying initial state."
        ) from exc

    # Check that none of the required locale lines are present yet.
    for expected_line in LOCALE_LINES:
        assert expected_line not in bashrc_content, (
            f"The line '{expected_line}' is already present in "
            f"{_nice_path(USER_BASHRC)}.  The student’s script must be the "
            "one to introduce these locale variables."
        )


def test_no_apply_script_executable_flag():
    """
    The executable bit on the (currently non-existent) apply_settings.sh
    script must, of course, not be present.  This test ensures we are not
    accidentally finding a leftover file with executable permissions.
    """
    assert not APPLY_SCRIPT.exists(), (
        f"Unexpected script found: {_nice_path(APPLY_SCRIPT)}. "
        "The student must create this file themselves."
    )
    # If by any chance it *does* exist, prevent a false pass due to the
    # earlier assertion by additionally checking mode bits.
    if APPLY_SCRIPT.exists():
        mode = APPLY_SCRIPT.stat().st_mode
        assert not (mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)), (
            f"{_nice_path(APPLY_SCRIPT)} already has execute permissions set. "
            "The file should not exist at all before the task begins."
        )