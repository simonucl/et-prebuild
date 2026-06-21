# test_initial_state.py
#
# This pytest suite validates the *initial* on-disk state that must be
# present before the student performs any action.  It checks that:
#
# 1. The expected backup directory tree exists.
# 2. The required files are present and are **empty** regular files.
# 3. The integrity-reference file exists and contains the correct,
#    precisely-formatted SHA-256 sums.
#
# NOTE:  We deliberately **do not** test for the post-task artefact
# /home/user/verification.log (or any other output).  Those checks will be
# performed by a different test stage after the student’s script runs.
#
# Only stdlib + pytest are used, as required.

import hashlib
from pathlib import Path

import pytest

HOME = Path("/home/user")
BACKUP_DIR = HOME / "backups" / "daily"
BASELINE_FILE = HOME / "baselines" / "daily.sha256"

EXPECTED_FILES = {
    "db.dump": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "config.tar.gz": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
}


def sha256_of(path: Path) -> str:
    """Compute the SHA-256 hex digest of a file without reading it all at once."""
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def read_baseline() -> dict:
    """
    Read /home/user/baselines/daily.sha256 and return a mapping of
    {filename: checksum}.  Lines must match the format
    '<sha256><two spaces><relative-file-name>'
    """
    baseline = {}
    with BASELINE_FILE.open("rt", encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            # Strip only the trailing '\n'; internal spaces are significant.
            if not line.endswith("\n"):
                raise AssertionError(
                    f"{BASELINE_FILE} line {lineno} is missing the trailing newline"
                )
            stripped = line[:-1]  # remove '\n'
            parts = stripped.split("  ")  # two spaces
            if len(parts) != 2:
                raise AssertionError(
                    f"{BASELINE_FILE} line {lineno} should contain exactly TWO spaces "
                    f"between checksum and filename; found: {repr(stripped)}"
                )
            checksum, filename = parts
            baseline[filename] = checksum
    return baseline


@pytest.mark.parametrize("filename", EXPECTED_FILES.keys())
def test_backup_file_presence_and_empty(filename):
    fpath = BACKUP_DIR / filename
    assert fpath.exists(), f"Required file {fpath} is missing"
    assert fpath.is_file(), f"{fpath} exists but is not a regular file"
    size = fpath.stat().st_size
    assert size == 0, f"{fpath} should be empty (0 bytes) but is {size} bytes"


def test_backup_directory_exists():
    assert BACKUP_DIR.exists(), f"Backup directory {BACKUP_DIR} does not exist"
    assert BACKUP_DIR.is_dir(), f"{BACKUP_DIR} exists but is not a directory"


def test_baseline_file_exists():
    assert BASELINE_FILE.exists(), f"Baseline file {BASELINE_FILE} is missing"
    assert BASELINE_FILE.is_file(), f"{BASELINE_FILE} exists but is not a regular file"


def test_baseline_contents():
    baseline_map = read_baseline()

    # Must contain exactly the expected entries—no more, no less.
    expected_set = set(EXPECTED_FILES.keys())
    actual_set = set(baseline_map.keys())
    assert (
        actual_set == expected_set
    ), f"{BASELINE_FILE} should reference files {sorted(expected_set)} but references {sorted(actual_set)}"

    # Verify each checksum string is of correct length/format and matches expectation.
    for fname, checksum in baseline_map.items():
        expected_checksum = EXPECTED_FILES[fname]
        assert (
            checksum == expected_checksum
        ), f"Checksum for {fname} in {BASELINE_FILE} should be {expected_checksum}, got {checksum}"
        assert (
            len(checksum) == 64 and all(c in "0123456789abcdef" for c in checksum)
        ), f"Checksum '{checksum}' for {fname} is not a valid 64-char hex SHA-256 digest"


def test_checksums_match_baseline():
    baseline_map = read_baseline()

    mismatches = []
    for fname, recorded_checksum in baseline_map.items():
        fpath = BACKUP_DIR / fname
        computed = sha256_of(fpath)
        if computed != recorded_checksum:
            mismatches.append((fname, recorded_checksum, computed))

    assert (
        not mismatches
    ), "Checksum mismatch(es): " + ", ".join(
        f"{fname}: expected {rec} but got {got}" for fname, rec, got in mismatches
    )