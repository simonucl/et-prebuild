# test_initial_state.py
#
# This pytest suite validates that the filesystem is in its **initial**,
# pre-task state for the “DevSecOps time & locale policy” exercise.
#
# NOTHING the student is asked to create should exist **yet**:
#
#   • /home/user/devsecops-config/time-locale/01-timezone.conf
#   • /home/user/devsecops-config/time-locale/02-locale.conf
#   • /home/user/devsecops-config/change-log.txt
#
# If any of those paths already exist (as files or directories), the
# environment is *not* pristine and the tests must fail with a clear
# explanation so the student knows what to clean up before proceeding.
#
# Only Python’s stdlib and pytest are used, per instructions.

import os
import pathlib
import stat

import pytest

HOME = pathlib.Path("/home/user")
ROOT_DIR = HOME / "devsecops-config"
TIME_LOCALE_DIR = ROOT_DIR / "time-locale"

FILE_TIMEZONE = TIME_LOCALE_DIR / "01-timezone.conf"
FILE_LOCALE = TIME_LOCALE_DIR / "02-locale.conf"
FILE_CHANGELOG = ROOT_DIR / "change-log.txt"


@pytest.mark.parametrize(
    "path",
    [
        pytest.param(FILE_TIMEZONE, id="01-timezone.conf must be absent"),
        pytest.param(FILE_LOCALE, id="02-locale.conf must be absent"),
        pytest.param(FILE_CHANGELOG, id="change-log.txt must be absent"),
    ],
)
def test_required_files_do_not_exist(path: pathlib.Path):
    """
    Ensure that none of the required artifacts are present *before* the student
    performs the task.  If any path exists (file, directory, or other), the
    environment is considered polluted.
    """
    assert not path.exists(), (
        f"Pre-task check failed: {path} already exists but it should NOT be present "
        "yet.  Please remove or rename it before attempting the exercise."
    )


def test_time_locale_directory_absent_or_empty():
    """
    The `time-locale` directory itself should not exist at this stage.
    If it does exist (e.g., accidental creation), it must be completely
    empty so as not to interfere with the task.
    """
    if not TIME_LOCALE_DIR.exists():
        # Ideal pristine state: directory absent.
        return

    # Directory exists – make sure it is empty and *is* a directory.
    assert TIME_LOCALE_DIR.is_dir(), (
        f"{TIME_LOCALE_DIR} exists but is not a directory; remove/rename it."
    )

    contents = list(TIME_LOCALE_DIR.iterdir())
    assert (
        len(contents) == 0
    ), (
        f"{TIME_LOCALE_DIR} should be empty before starting the exercise, "
        f"but it already contains: {', '.join(str(p) for p in contents)}"
    )


def test_root_directory_absent_or_pristine():
    """
    The top-level `/home/user/devsecops-config` directory should either not
    exist at all or, if it does, it must not already contain any of the files
    the student is supposed to create in this exercise.
    """
    if not ROOT_DIR.exists():
        # Ideal pristine state: directory absent.
        return

    assert ROOT_DIR.is_dir(), (
        f"{ROOT_DIR} exists but is not a directory; remove/rename it."
    )

    forbidden = {
        FILE_TIMEZONE,
        FILE_LOCALE,
        FILE_CHANGELOG,
    }

    for path in forbidden:
        assert (
            not path.exists()
        ), (
            f"Pre-task check failed: {path} already exists. "
            "Please remove or rename it before starting the exercise."
        )


def test_paths_are_within_home_user():
    """
    Sanity check: Ensure we are testing the expected absolute paths that live
    under /home/user.  If /home/user itself is missing, flag it—most likely the
    environment is mis-configured.
    """
    assert HOME.exists(), (
        "/home/user does not exist on this system.  The exercise assumes all "
        "work occurs under /home/user; please create that directory or adjust "
        "the environment accordingly."
    )

    assert HOME.is_dir(), (
        "/home/user exists but is not a directory; unexpected filesystem state."
    )