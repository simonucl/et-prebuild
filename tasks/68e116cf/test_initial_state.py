# test_initial_state.py
"""
PyTest suite that verifies the **initial** state of the OS / filesystem
BEFORE the student starts working on the “automation-workflow” task.

Nothing from the target directory tree (/home/user/workflow/…) should
exist yet.  These checks guarantee that the student begins with a clean
slate and that any later artefacts are indeed created by their solution.

If any of the asserted-to-be-absent paths already exist, the test will
fail with an explicit, human-readable message.
"""
import os
import stat
import pytest

BASE_DIR = "/home/user/workflow"

PATHS = {
    "base": BASE_DIR,
    "config_dir": os.path.join(BASE_DIR, "config"),
    "settings_file": os.path.join(BASE_DIR, "config", "regional_settings.sh"),
    "scripts_dir": os.path.join(BASE_DIR, "scripts"),
    "helper_script": os.path.join(BASE_DIR, "scripts", "generate_timestamp.sh"),
    "logs_dir": os.path.join(BASE_DIR, "logs"),
    "log_file": os.path.join(BASE_DIR, "logs", "time_check.log"),
}

@pytest.mark.parametrize("path_key", PATHS.keys())
def test_paths_do_not_exist_yet(path_key):
    """
    Assert that none of the files or directories that the student is meant
    to create are present at the start.

    Each param corresponds to one absolute path defined in the PATHS dict.
    """
    path = PATHS[path_key]
    assert not os.path.exists(path), (
        f"The path {path!r} already exists, but the environment is expected "
        "to be clean before the student begins.  Please remove it so the "
        "assignment starts from a known empty state."
    )

def test_no_executable_bits_set_on_missing_helper_script():
    """
    As an extra sanity check, make sure an executable helper script does not
    accidentally pre-exist with the desired permission bits.

    This guards against a scenario where a stale artefact is lying around.
    """
    script_path = PATHS["helper_script"]
    if os.path.exists(script_path):
        mode = os.stat(script_path).st_mode
        is_executable = bool(mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
        assert not is_executable, (
            f"Unexpected executable file found at {script_path!r}.  The script "
            "should not exist before the student creates it."
        )
    else:
        # Path doesn't exist — which is what we want.
        assert True