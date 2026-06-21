# test_initial_state.py
#
# This test-suite validates that the filesystem is in the expected, pristine
# state *before* the student’s auditing script is executed.  It checks for
# the presence (or absence) of specific files/directories and verifies their
# permission bits so that subsequent grading logic can rely on a known
# baseline.

import os
import stat
import pytest


SEARCH_ROOT = "/home/user"


@pytest.mark.parametrize(
    "path, object_type, should_be_world_writable",
    [
        # World-writable objects that **must** be present
        ("/home/user/public.txt", "file", True),
        ("/home/user/projects/test_project/tmp_data.log", "file", True),
        ("/home/user/www", "dir", True),
        # Objects that must exist but must *NOT* be world-writable
        ("/home/user/notes.txt", "file", False),
        ("/home/user/projects/test_project/main.py", "file", False),
        ("/home/user/projects/private_secret", "dir", False),
    ],
)
def test_object_presence_and_permissions(path, object_type, should_be_world_writable):
    """Ensure each listed object exists with the correct world-writable flag."""
    assert os.path.exists(
        path
    ), f"Required object '{path}' is missing; the fixture setup is incorrect."

    if object_type == "file":
        assert os.path.isfile(
            path
        ), f"Expected '{path}' to be a regular file, but it is not."
    elif object_type == "dir":
        assert os.path.isdir(
            path
        ), f"Expected '{path}' to be a directory, but it is not."
    else:
        pytest.fail(f"BUG in test definition: unknown object_type '{object_type}'")

    mode = os.stat(path).st_mode
    is_world_writable = bool(mode & stat.S_IWOTH)

    if should_be_world_writable:
        assert (
            is_world_writable
        ), f"Object '{path}' is expected to be world-writable but is not."
    else:
        assert (
            not is_world_writable
        ), f"Object '{path}' must *not* be world-writable, but it is."


def test_search_root_is_single_filesystem():
    """
    Sanity-check that SEARCH_ROOT exists and is a directory; later tasks rely on it.

    Note: We deliberately do *not* test the presence of /home/user/audit or any
    output files, as per the grading instructions.
    """
    assert os.path.isdir(
        SEARCH_ROOT
    ), f"Search root '{SEARCH_ROOT}' is missing or not a directory."