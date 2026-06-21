# test_initial_state.py
#
# This test-suite verifies that the workspace is **clean** before the student
# begins the task of generating the “mini-SDK”.  None of the artefacts that the
# student is expected to create later should exist yet.  If any of them are
# already present, the tests will fail with a clear, actionable message.

import os
import stat
import pytest

HOME = "/home/user"

# --------------------------------------------------------------------------- #
# Sanity check: the user's home directory itself must exist and be a directory
# --------------------------------------------------------------------------- #
def test_home_directory_exists():
    assert os.path.isdir(HOME), (
        f"Expected the home directory {HOME!r} to exist and be a directory, "
        "but it is missing."
    )


# --------------------------------------------------------------------------- #
# The “mini-SDK” paths that must *not* exist before the student starts working
# --------------------------------------------------------------------------- #
SDK_DIR = os.path.join(HOME, "api_samples")
REQUIRED_PATHS = [
    SDK_DIR,
    os.path.join(SDK_DIR, "README.md"),
    os.path.join(SDK_DIR, "curl_commands.log"),
    os.path.join(SDK_DIR, "responses"),
    os.path.join(SDK_DIR, "responses", "get_posts_1.json"),
    os.path.join(SDK_DIR, "responses", "get_comments_post1.json"),
    os.path.join(SDK_DIR, "responses", "post_posts.json"),
    os.path.join(SDK_DIR, "responses", "put_posts_1.json"),
    os.path.join(SDK_DIR, "responses", "delete_posts_1.json"),
]

@pytest.mark.parametrize("path", REQUIRED_PATHS)
def test_sdk_paths_do_not_exist_yet(path):
    assert not os.path.exists(path), (
        f"The path {path!r} should NOT exist at the initial state. "
        "Please remove it so the student can create it as part of the task."
    )


# --------------------------------------------------------------------------- #
# Defensive check: if the base directory *does* exist for some reason, ensure
# it is empty so that it does not contain pre-existing artefacts that could
# interfere with the assignment.
# --------------------------------------------------------------------------- #
def test_api_samples_dir_empty_if_it_exists():
    if not os.path.exists(SDK_DIR):
        pytest.skip(f"{SDK_DIR!r} does not exist — no need to check its contents.")

    # The directory exists; it must be empty.
    contents = os.listdir(SDK_DIR)
    assert contents == [], (
        f"The directory {SDK_DIR!r} already exists but is expected to be empty "
        "before the student starts. Found unexpected files/directories: "
        f"{', '.join(contents)}"
    )


# --------------------------------------------------------------------------- #
# Ensure that no response files are masquerading as directories (or vice versa)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("path", REQUIRED_PATHS)
def test_required_paths_not_wrong_type(path):
    # If a path does exist (which should already fail the earlier test), make
    # sure it is not of an unexpected type (e.g., directory where a file should be).
    if not os.path.exists(path):
        pytest.skip("Path does not exist, as expected.")

    is_expected_directory = path.endswith("responses")
    mode = os.stat(path).st_mode

    if is_expected_directory:
        assert stat.S_ISDIR(mode), (
            f"Expected {path!r} to be a directory, but it is a file."
        )
    else:
        assert stat.S_ISREG(mode), (
            f"Expected {path!r} to be a regular file, but it is a directory."
        )