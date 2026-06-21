# test_initial_state.py
#
# These tests assert that the operating-system / filesystem is in the
# EXPECTED **initial** state – i.e. *before* the student carries out any
# steps described in the task.  Nothing created by the assignment should be
# present yet.  If any of the target files already exist, or already have
# the required permissions / contents, the test-suite will fail with a clear
# message, indicating that the environment is “dirty” and must be reset.

import os
import stat
import pytest

HOME = "/home/user"
PIPELINE_DIR = os.path.join(HOME, "pipeline")

# Absolute paths that MUST NOT exist at the beginning of the exercise
TARGET_PATHS = {
    "build_env": os.path.join(PIPELINE_DIR, "config", "build_env.sh"),
    "verify_script": os.path.join(PIPELINE_DIR, "scripts", "verify_locale.sh"),
    "log_file": os.path.join(PIPELINE_DIR, "logs", "locale_check.log"),
}


@pytest.mark.parametrize("path_key", sorted(TARGET_PATHS.keys()))
def test_target_paths_absent(path_key):
    """
    The core requirement for the *initial* state is that none of the files
    the student is supposed to create are present yet.  The assignment
    explicitly instructs the student to *create* or *overwrite* these
    artefacts, so their prior existence would indicate an invalid starting
    point for the exercise.
    """
    path = TARGET_PATHS[path_key]
    assert not os.path.exists(path), (
        f"Pre-exercise sanity check failed: the path {path!r} already exists. "
        "The working directory must be clean before the student begins."
    )


def test_verify_locale_not_executable():
    """
    Even if a stray verify_locale.sh file somehow exists, it must not already
    have the executable bit set in the initial state.  A pre-existing,
    executable script would defeat the purpose of the task.
    """
    script_path = TARGET_PATHS["verify_script"]

    if not os.path.exists(script_path):
        pytest.skip("verify_locale.sh does not exist yet (expected)")

    st = os.stat(script_path)
    is_executable = bool(st.st_mode & stat.S_IXUSR)
    assert not is_executable, (
        f"Pre-exercise sanity check failed: {script_path!r} is already "
        "marked as executable."
    )