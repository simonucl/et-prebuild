# test_initial_state.py
#
# This pytest suite validates the state of the filesystem **before**
# the student executes any command.  It verifies that the storage sandbox
# contains exactly the five regular files described in the task
# description—no more and no fewer—and that their sizes are correct.

import os
import stat
import pytest

STORAGE_DIR = "/home/user/storage_sandbox"

# Mapping of expected absolute paths to their exact sizes in bytes.
EXPECTED_FILES = {
    "/home/user/storage_sandbox/videos/movie.mp4": 10_485_760,
    "/home/user/storage_sandbox/docs/archive.zip": 7_340_032,
    "/home/user/storage_sandbox/big_iso.iso": 5_555_555,
    "/home/user/storage_sandbox/videos/short.mov": 2_097_152,
    "/home/user/storage_sandbox/docs/notes.txt": 1_024,
}

@pytest.fixture(scope="module")
def discovered_regular_files():
    """
    Walk STORAGE_DIR recursively and return a dict {absolute_path: size}
    for every *regular* (non-symlink) file encountered.
    """
    regular_files = {}
    for root, _dirs, files in os.walk(STORAGE_DIR):
        for name in files:
            abs_path = os.path.join(root, name)
            try:
                st = os.lstat(abs_path)
            except FileNotFoundError:
                # If the file disappears between discovery and stat, treat it as missing.
                continue
            # Only count true regular files (not symlinks, FIFOs, etc.)
            if stat.S_ISREG(st.st_mode) and not stat.S_ISLNK(st.st_mode):
                regular_files[abs_path] = st.st_size
    return regular_files


def test_storage_directory_exists():
    assert os.path.exists(STORAGE_DIR), (
        f"Required directory {STORAGE_DIR!r} does not exist."
    )
    assert os.path.isdir(STORAGE_DIR), (
        f"Expected {STORAGE_DIR!r} to be a directory."
    )


@pytest.mark.parametrize("path,size", EXPECTED_FILES.items())
def test_expected_file_present_with_correct_size(path, size):
    assert os.path.exists(path), f"Expected file {path!r} is missing."
    assert os.path.isfile(path), f"{path!r} exists but is not a regular file."
    actual_size = os.path.getsize(path)
    assert (
        actual_size == size
    ), f"File {path!r} has size {actual_size}, expected {size} bytes."


def test_no_unexpected_regular_files(discovered_regular_files):
    """
    The directory must contain exactly the five expected regular files.
    """
    discovered_set = set(discovered_regular_files.keys())
    expected_set = set(EXPECTED_FILES.keys())

    missing = expected_set - discovered_set
    extra = discovered_set - expected_set

    msg_parts = []
    if missing:
        msg_parts.append("Missing files:\n  " + "\n  ".join(sorted(missing)))
    if extra:
        msg_parts.append("Unexpected extra files:\n  " + "\n  ".join(sorted(extra)))

    assert not missing and not extra, (
        "Filesystem does not match the expected state:\n" + "\n".join(msg_parts)
    )

    # As a final sanity check, ensure the sizes of discovered files match the expectation.
    for path in expected_set:
        expected_size = EXPECTED_FILES[path]
        discovered_size = discovered_regular_files[path]
        assert discovered_size == expected_size, (
            f"Size mismatch for {path!r}: expected {expected_size}, got {discovered_size}"
        )