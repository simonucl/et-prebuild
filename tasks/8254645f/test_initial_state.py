# test_initial_state.py
#
# This test-suite is executed **before** the candidate performs any action.
# It verifies that none of the artefacts the exercise asks for are already
# present.  If any of them are found, the initial state is considered
# polluted and the tests will fail with a descriptive error so the student
# (or the automated environment) can start from a clean slate.
#
# NOTE: Only the Python standard library and pytest are used, in accordance
# with the grading infrastructure requirements.

import os
import stat
import pytest

HOME = "/home/user"
SRE_DIR = os.path.join(HOME, "sre")

SERVICES_LST = os.path.join(SRE_DIR, "services.lst")
CHECK_SH = os.path.join(SRE_DIR, "check_services.sh")
UPTIME_LOG = os.path.join(SRE_DIR, "uptime.log")

@pytest.fixture(scope="module")
def paths():
    """
    A convenience fixture that returns a dictionary with all paths that must
    NOT exist in the initial state.
    """
    return {
        "sre_dir": SRE_DIR,
        "services_lst": SERVICES_LST,
        "check_services_sh": CHECK_SH,
        "uptime_log": UPTIME_LOG,
    }


def test_home_directory_exists():
    """
    Sanity-check: the non-privileged user's home directory **must** already
    exist so that subsequent tasks can create artefacts underneath it.
    """
    assert os.path.isdir(HOME), (
        f"Expected the base home directory {HOME!r} to exist, "
        "but it is missing."
    )


def test_sre_directory_absent(paths):
    """
    Before the student begins, /home/user/sre must NOT exist.  A pre-existing
    directory would indicate a dirty environment or a previous run leaking
    state.
    """
    sre_dir = paths["sre_dir"]
    assert not os.path.exists(sre_dir), (
        f"The directory {sre_dir!r} should NOT exist at the start of the "
        "exercise.  Please remove it before beginning."
    )


@pytest.mark.parametrize(
    "file_key,description",
    [
        ("services_lst", "/home/user/sre/services.lst"),
        ("check_services_sh", "/home/user/sre/check_services.sh"),
        ("uptime_log", "/home/user/sre/uptime.log"),
    ],
)
def test_expected_files_absent(paths, file_key, description):
    """
    None of the target files should exist prior to the student's work.
    Explicitly check each one so that failures are easy to interpret.
    """
    file_path = paths[file_key]
    assert not os.path.exists(file_path), (
        f"The file {file_path!r} should NOT exist before the exercise starts. "
        f"Found an unexpected {('executable' if os.access(file_path, os.X_OK) else 'file')}."
    )


def test_no_leftover_executable_bit_on_missing_script(paths):
    """
    Guard against a corner case: if the directory tree somehow exists but the
    main script was deleted, a dangling inode with the same name could still
    be on disk and marked executable.  This test asserts that either the file
    is entirely absent (preferred) or, if somehow present, that it's not yet
    executable.  In either case the environment is considered clean enough
    for the candidate to continue.
    """
    script = paths["check_services_sh"]
    if os.path.exists(script):
        mode = os.stat(script).st_mode
        assert not (mode & stat.S_IXUSR), (
            f"The script {script!r} unexpectedly has the executable bit set. "
            "Start from a clean state before proceeding."
        )