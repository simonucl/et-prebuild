# test_initial_state.py
#
# This test-suite verifies that the *starting* operating-system / filesystem
# conditions are clean, i.e. the artefacts that the student is asked to create
# do NOT already exist in their final, fully-hardened form.  This guarantees
# that the exercise is still meaningful before the student begins any work.

import os
import stat
import pytest

HOME = "/home/user"
WORKFLOWS_DIR = os.path.join(HOME, "workflows")
RUN_SH = os.path.join(WORKFLOWS_DIR, "run.sh")
LOG_FILE = os.path.join(HOME, "permission_log.txt")

EXPECTED_DIR_MODE = 0o750
EXPECTED_FILE_MODE = 0o740
EXPECTED_LOG_CONTENT = (
    f"{WORKFLOWS_DIR} 750\n"
    f"{RUN_SH} 740\n"
)


def _mode(path: str) -> int:
    """
    Return the permission bits (e.g. 0o755) of *path*.
    If *path* does not exist, raise FileNotFoundError.
    """
    st = os.stat(path, follow_symlinks=True)
    return stat.S_IMODE(st.st_mode)


def test_workflows_directory_not_yet_hardened():
    """
    The directory /home/user/workflows must either:

    * not exist at all, OR
    * exist but NOT already be set to exactly 750.

    If it already exists *and* has 750, the setup is already finished,
    which should not be the case before the student works on the task.
    """
    if not os.path.exists(WORKFLOWS_DIR):
        pytest.skip(f"{WORKFLOWS_DIR!r} does not exist yet (this is fine).")

    # It exists — make sure it's a directory.
    assert os.path.isdir(WORKFLOWS_DIR), (
        f"{WORKFLOWS_DIR} exists but is not a directory. "
        "Please remove or rename it before starting the exercise."
    )

    current_mode = _mode(WORKFLOWS_DIR)
    assert current_mode != EXPECTED_DIR_MODE, (
        f"{WORKFLOWS_DIR} already has mode 0o{EXPECTED_DIR_MODE:o} "
        "(exercise appears to be completed beforehand)."
    )


def test_run_sh_not_yet_present_or_hardened():
    """
    /home/user/workflows/run.sh must either not exist, or if it exists,
    must NOT already be a regular file with mode 740.
    """
    if not os.path.exists(RUN_SH):
        pytest.skip(f"{RUN_SH!r} does not exist yet (this is fine).")

    # It exists — ensure it is a regular file.
    assert os.path.isfile(RUN_SH), (
        f"{RUN_SH} exists but is not a regular file. "
        "Please remove or rename it before starting the exercise."
    )

    current_mode = _mode(RUN_SH)
    assert current_mode != EXPECTED_FILE_MODE, (
        f"{RUN_SH} already has mode 0o{EXPECTED_FILE_MODE:o} "
        "(exercise appears to be completed beforehand)."
    )


def test_permission_log_not_already_finalised():
    """
    The log file /home/user/permission_log.txt must either be absent or
    contain something other than the final two-line specification.
    """
    if not os.path.exists(LOG_FILE):
        pytest.skip(f"{LOG_FILE!r} does not exist yet (this is fine).")

    assert os.path.isfile(LOG_FILE), (
        f"{LOG_FILE} exists but is not a regular file. "
        "Please remove or rename it before starting the exercise."
    )

    try:
        with open(LOG_FILE, "rt", encoding="utf-8") as fh:
            content = fh.read()
    except Exception as exc:
        pytest.skip(f"Could not read {LOG_FILE}: {exc}")

    assert content != EXPECTED_LOG_CONTENT, (
        f"{LOG_FILE} already contains the final expected content:\n{EXPECTED_LOG_CONTENT!r}\n"
        "The exercise appears to have been completed beforehand."
    )