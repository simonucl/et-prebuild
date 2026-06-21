# test_initial_state.py
#
# This pytest suite verifies that the workspace is **clean** before the
# student begins the exercise.  None of the files or directories that the
# student is expected to create (see the task description) should exist yet.
#
# If any of them are found, the tests will fail with a clear explanation so
# the learner can remove the pre-existing artifacts and start from a known,
# reproducible baseline.

import os
import stat
import pytest

BUNDLE_DIR = "/home/user/security_bundle"
APPLY_SCRIPT = os.path.join(BUNDLE_DIR, "apply_firewall.sh")
LOG_FILE = os.path.join(BUNDLE_DIR, "firewall_execution.log")


def _path_readable(path: str) -> str:
    """
    Return a human-readable representation of `path` that states whether the
    object is a directory, file, or something else.  Used only for error
    messaging.
    """
    if os.path.isdir(path):
        return f"directory '{path}'"
    if os.path.isfile(path):
        return f"file '{path}'"
    if os.path.exists(path):
        return f"object '{path}' (neither regular file nor directory)"
    return f"nothing at '{path}'"


@pytest.mark.order(1)
def test_bundle_directory_absent():
    """
    The bundle directory must **not** exist yet.  The student will create it
    during the exercise.
    """
    assert not os.path.exists(BUNDLE_DIR), (
        f"Pre-existing {_path_readable(BUNDLE_DIR)} detected.\n"
        "Please remove it so you can follow the exercise steps from a clean "
        "state."
    )


@pytest.mark.order(2)
def test_apply_script_absent():
    """
    The apply_firewall.sh script must **not** exist before the exercise begins.
    """
    assert not os.path.exists(APPLY_SCRIPT), (
        f"Unexpected {_path_readable(APPLY_SCRIPT)} found.  Remove it before "
        "starting the exercise."
    )


@pytest.mark.order(3)
def test_log_file_absent():
    """
    The firewall_execution.log template must **not** exist before the exercise.
    """
    assert not os.path.exists(LOG_FILE), (
        f"Unexpected {_path_readable(LOG_FILE)} found.  Remove it before "
        "starting the exercise."
    )


@pytest.mark.order(4)
def test_no_stray_security_bundle_items(tmp_path_factory):
    """
    Even if /home/user/security_bundle/ does not exist, ensure no partial or
    misspelled variants are present (e.g. 'security-bundle', 'Security_Bundle',
    etc.).  This keeps the workspace tidy and avoids accidental reuse of old
    artifacts.
    """
    parent_dir = os.path.dirname(BUNDLE_DIR)
    if not os.path.isdir(parent_dir):
        # If /home/user itself is missing something is very wrong, but we
        # tolerate it here to avoid false negatives in exotic environments.
        pytest.skip(f"Parent directory '{parent_dir}' is not available.")

    # Look for any directory names that start with 'security' in /home/user
    for entry in os.listdir(parent_dir):
        if entry.lower().startswith("security") and entry != "security_bundle":
            candidate = os.path.join(parent_dir, entry)
            assert not os.path.exists(candidate), (
                f"Stray {_path_readable(candidate)} found.  Please clean up "
                "any leftover directories from previous attempts."
            )