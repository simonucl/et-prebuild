# test_initial_state.py
#
# This test-suite validates the *initial* state of the filesystem
# before the student attempts to create /home/user/integrity_logs/backup_check.log.
# It purposely does NOT mention (or test for) the output directory /home/user/integrity_logs
# or the eventual log file, because those do **not** have to exist yet.
#
# The checks performed are:
#   • Required directories and files exist under /home/user/daily_backup.
#   • /home/user/reference/sha256sums.txt exists.
#   • The reference file contains exactly three SHA-256 digests, each followed by
#     two spaces and the correct *relative* path.
#   • The digests in the reference file match the actual digests of the
#     corresponding files.
#
# If any assertion fails, the error message will describe precisely what
# is missing or inconsistent.

import hashlib
import os
from pathlib import Path

import pytest

HOME = Path("/home/user")

# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------
def sha256_of(path: Path) -> str:
    """Return the hexadecimal SHA-256 digest of the given file."""
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# -----------------------------------------------------------------------------
# Expected paths relative to HOME
# -----------------------------------------------------------------------------
DAILY_BACKUP = HOME / "daily_backup"
REFERENCE_FILE = HOME / "reference" / "sha256sums.txt"

RELATIVE_PATHS = [
    "docs/report.txt",
    "images/logo.png",
    "data/data.csv",
]

ABSOLUTE_PATHS = [DAILY_BACKUP / rel for rel in RELATIVE_PATHS]


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------
def test_daily_backup_directory_exists():
    assert DAILY_BACKUP.is_dir(), (
        f"Required directory {DAILY_BACKUP} does not exist."
    )


@pytest.mark.parametrize("abs_path", ABSOLUTE_PATHS)
def test_backup_files_exist(abs_path: Path):
    assert abs_path.is_file(), f"Required file {abs_path} is missing."


def test_reference_file_exists():
    assert REFERENCE_FILE.is_file(), (
        f"Reference digest file {REFERENCE_FILE} is missing."
    )


def test_reference_file_format_and_integrity():
    """
    1. The reference file must contain exactly three lines.
    2. Each line must follow the 'sha256  <two spaces>  relative/path' format.
    3. The set of relative paths must be exactly the expected set.
    4. Each digest must match the actual digest of its corresponding file.
    """
    lines = REFERENCE_FILE.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 3, (
        f"{REFERENCE_FILE} must contain exactly 3 lines, found {len(lines)}."
    )

    digest_map = {}
    for idx, line in enumerate(lines, start=1):
        # The 'sha256sum' utility separates digest and path with two spaces.
        parts = line.split("  ")
        assert len(parts) == 2, (
            f"Line {idx} in {REFERENCE_FILE} is malformed: "
            f"expected exactly two spaces between digest and path."
        )
        digest, rel_path = parts
        # Basic validation of digest length/content.
        assert len(digest) == 64 and all(c in "0123456789abcdef" for c in digest), (
            f"Line {idx} in {REFERENCE_FILE} contains an invalid SHA-256 digest."
        )
        assert not rel_path.startswith("/"), (
            f"Line {idx} in {REFERENCE_FILE} uses an absolute path; "
            f"relative path expected."
        )
        digest_map[rel_path] = digest

    # Ensure we have the exact set of paths we expect.
    expected_set = set(RELATIVE_PATHS)
    found_set = set(digest_map)
    assert found_set == expected_set, (
        f"{REFERENCE_FILE} must list the paths {sorted(expected_set)}, "
        f"but it lists {sorted(found_set)}."
    )

    # Finally, confirm each digest matches the real file.
    for rel_path, expected_digest in digest_map.items():
        abs_path = DAILY_BACKUP / rel_path
        assert abs_path.is_file(), (
            f"{abs_path} listed in {REFERENCE_FILE} is missing."
        )
        actual_digest = sha256_of(abs_path)
        assert actual_digest == expected_digest, (
            f"Digest mismatch for {abs_path}: "
            f"reference has {expected_digest}, actual is {actual_digest}."
        )


# The test suite purposefully stops here: it does *not* check for
# /home/user/integrity_logs or backup_check.log, because those are the
# artefacts the student is expected to create.