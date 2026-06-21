# test_initial_state.py

"""
Pytest suite that validates the starting filesystem state **before**
the student runs their solution script.

Checks performed:
1. The required directories exist and are directories.
2. The binary-repository directory contains the exact three expected files.
3. Each file is the expected size and contains the expected repeated byte
   pattern (A, B, or C).

If any check fails, the assertion message explains precisely what is wrong.
"""

import os
import stat
import pytest

HOME = "/home/user"
BINREPO_DIR = os.path.join(HOME, "repos", "binrepo")
REPORTS_DIR = os.path.join(HOME, "reports")

# Expected files: name -> (size_in_bytes, byte_value)
EXPECTED_FILES = {
    "alpha.bin": (100, b"A"),
    "beta.bin":  (200, b"B"),
    "gamma.bin": (300, b"C"),
}


def test_required_directories_exist_and_are_dirs():
    """
    The two top-level directories that the task depends on must exist
    and must be directories.
    """
    for path in (BINREPO_DIR, REPORTS_DIR):
        assert os.path.exists(path), f"Required directory {path!r} is missing."
        assert os.path.isdir(path), f"{path!r} exists but is not a directory."


def test_binrepo_contains_only_expected_files():
    """
    /home/user/repos/binrepo should contain exactly the three expected
    binary files and nothing else (aside from . and .. entries).
    """
    present = sorted(
        f
        for f in os.listdir(BINREPO_DIR)
        if os.path.isfile(os.path.join(BINREPO_DIR, f))
    )
    expected = sorted(EXPECTED_FILES.keys())
    assert present == expected, (
        f"/home/user/repos/binrepo contains unexpected file set.\n"
        f"Expected: {expected}\n"
        f"Found   : {present}"
    )


@pytest.mark.parametrize("filename,meta", EXPECTED_FILES.items())
def test_each_file_has_expected_size_and_content(filename, meta):
    """
    For each file, verify:
      • it exists and is a regular file
      • its size in bytes matches the spec
      • its entire content is the repeated expected byte
    """
    expected_size, expected_byte = meta
    path = os.path.join(BINREPO_DIR, filename)

    # Existence and type
    assert os.path.exists(path), f"Expected file {path!r} is missing."
    assert os.path.isfile(path), f"{path!r} exists but is not a regular file."

    # Size check
    actual_size = os.path.getsize(path)
    assert actual_size == expected_size, (
        f"{path!r} size mismatch: expected {expected_size} bytes, "
        f"found {actual_size} bytes."
    )

    # Content check (read in chunks for memory safety, though files are tiny)
    expected_chunk = expected_byte * 1024  # 1 KiB chunk of the same byte
    with open(path, "rb") as fh:
        remaining = expected_size
        while remaining:
            chunk = fh.read(min(1024, remaining))
            assert chunk, f"Unexpected EOF when reading {path!r}."
            # Build the reference chunk of the same length for comparison
            ref = expected_byte * len(chunk)
            assert chunk == ref, (
                f"{path!r} content mismatch: "
                f"expected only byte {expected_byte.decode()} repeated."
            )
            remaining -= len(chunk)

        # The next read must yield EOF
        assert fh.read(1) == b"", f"{path!r} has more data than expected."