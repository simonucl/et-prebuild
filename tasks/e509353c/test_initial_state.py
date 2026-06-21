# test_initial_state.py
"""
Pytest suite that validates the *initial* filesystem state for the
“end-of-day backup” exercise, before the student performs any action.

Only the items that must already exist are verified here.  Nothing about
the yet-to-be-created /home/user/backups directory (or its contents) is
checked in this file.
"""

import os
import stat
import pytest

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

ARTIFACT_ROOT = "/home/user/artifacts"
BIN_DIR       = os.path.join(ARTIFACT_ROOT, "bin")

EXPECTED_DIRS = {
    ARTIFACT_ROOT: 0o755,
    BIN_DIR:       0o755,
}

EXPECTED_FILES = {
    os.path.join(BIN_DIR, "cliapp"):        {"mode": 0o644, "size": 0,  "content": b""},
    os.path.join(BIN_DIR, "libhelper.so"):  {"mode": 0o644, "size": 0,  "content": b""},
    os.path.join(ARTIFACT_ROOT, "README.md"): {
        "mode": 0o644,
        "size": 18,                              # len(b"Demo artifact set\n")
        "content": b"Demo artifact set\n",
    },
}


def _mode(path):
    """Return POSIX permission bits for a path, e.g. 0o755."""
    return stat.S_IMODE(os.stat(path, follow_symlinks=False).st_mode)


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("dpath,expected_mode", EXPECTED_DIRS.items())
def test_expected_directories_exist_with_correct_mode(dpath, expected_mode):
    assert os.path.exists(dpath), f"Required directory {dpath!r} is missing."
    assert os.path.isdir(dpath),  f"{dpath!r} exists but is not a directory."
    actual_mode = _mode(dpath)
    assert actual_mode == expected_mode, (
        f"Directory {dpath!r} has mode {oct(actual_mode)}, "
        f"expected {oct(expected_mode)}."
    )


@pytest.mark.parametrize("fpath,meta", EXPECTED_FILES.items())
def test_expected_files_exist_with_correct_mode_size_and_content(fpath, meta):
    assert os.path.exists(fpath), f"Required file {fpath!r} is missing."
    assert os.path.isfile(fpath), f"{fpath!r} exists but is not a regular file."

    # Permissions
    actual_mode = _mode(fpath)
    expected_mode = meta["mode"]
    assert actual_mode == expected_mode, (
        f"File {fpath!r} has mode {oct(actual_mode)}, "
        f"expected {oct(expected_mode)}."
    )

    # Size
    actual_size = os.path.getsize(fpath)
    expected_size = meta["size"]
    assert actual_size == expected_size, (
        f"File {fpath!r} has size {actual_size} bytes, "
        f"expected {expected_size} bytes."
    )

    # Content (read as binary to avoid newline translation surprises)
    with open(fpath, "rb") as fp:
        content = fp.read()
    expected_content = meta["content"]
    assert content == expected_content, (
        f"File {fpath!r} has unexpected contents.\n"
        f"Expected: {expected_content!r}\n"
        f"Actual:   {content!r}"
    )