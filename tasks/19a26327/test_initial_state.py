# test_initial_state.py
#
# This pytest suite asserts the *initial* state of the operating system
# before the student performs any actions for the deployment task.
#
# It intentionally verifies ONLY the prerequisites (the "given" part of
# the task) and does **not** check for the presence or absence of any of
# the artifacts the student is expected to create later (release
# directory, archive, log file, etc.).

import os
import stat
import pytest

HOME = "/home/user"
CURRENT_DIR = os.path.join(HOME, "app", "current")

EXPECTED_FILES = {
    "app.py": "# placeholder\n",
    "README.md": "Demo app\n",
}

EXPECTED_PERMS = 0o644  # rw-r--r--


@pytest.fixture(scope="module")
def current_dir_listing():
    """
    Return a dict mapping filename -> full path for everything found
    directly inside /home/user/app/current.
    """
    assert os.path.isdir(CURRENT_DIR), (
        f"Required directory {CURRENT_DIR!r} is missing."
    )

    listing = {}
    for name in os.listdir(CURRENT_DIR):
        full_path = os.path.join(CURRENT_DIR, name)
        listing[name] = full_path
    return listing


def test_current_dir_contains_only_expected_files(current_dir_listing):
    """
    The snapshot directory must contain *exactly* the two expected files,
    nothing more and nothing less.
    """
    expected_set = set(EXPECTED_FILES)
    actual_set = set(current_dir_listing)

    missing = expected_set - actual_set
    extra = actual_set - expected_set

    msg_parts = []
    if missing:
        msg_parts.append(f"missing files: {', '.join(sorted(missing))}")
    if extra:
        msg_parts.append(f"unexpected extra items: {', '.join(sorted(extra))}")

    assert not msg_parts, (
        f"/home/user/app/current should contain only {sorted(expected_set)}, "
        f"but {', '.join(msg_parts)}."
    )


@pytest.mark.parametrize("filename,expected_content", EXPECTED_FILES.items())
def test_file_contents_match_expected(current_dir_listing, filename, expected_content):
    """
    Verify that each file contains the expected single-line text.
    """
    path = current_dir_listing.get(filename)
    assert path, f"{filename!r} is missing from {CURRENT_DIR!r}."

    with open(path, "r", encoding="utf-8") as fp:
        data = fp.read()

    assert data == expected_content, (
        f"Contents of {path!r} do not match expected text."
    )


@pytest.mark.parametrize("filename", EXPECTED_FILES.keys())
def test_file_permissions_are_0644(current_dir_listing, filename):
    """
    Each file should have permissions 0644 (rw-r--r--).
    """
    path = current_dir_listing.get(filename)
    assert path, f"{filename!r} is missing from {CURRENT_DIR!r}."

    st_mode = os.lstat(path).st_mode
    perms = stat.S_IMODE(st_mode)
    assert perms == EXPECTED_PERMS, (
        f"Permissions for {path!r} are {oct(perms)}, expected {oct(EXPECTED_PERMS)}."
    )