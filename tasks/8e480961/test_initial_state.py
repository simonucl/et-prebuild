# test_initial_state.py
#
# Pytest suite that validates the operating-system state *before* the
# student’s solution runs.  It checks that the directory
# /home/user/audit_sample exists, contains exactly the expected four
# entries, and that each entry has the correct type and permission
# bits.  No assertions are made about any output files (e.g.,
# /home/user/permission_report.log).

import os
import stat
from pathlib import Path

import pytest

AUDIT_DIR = Path("/home/user/audit_sample")

# Mapping of entry name (exact basename) to a tuple:
#   (expected_type, expected_octal_mode)
#     expected_type is either "file" or "dir"
#     expected_octal_mode is an int such that oct(... & 0o777) == octal string
EXPECTED_ENTRIES = {
    "file1.conf": ("file", 0o644),
    "script.sh": ("file", 0o755),
    "secret.key": ("file", 0o600),
    "config": ("dir",  0o700),
}


def _mode_bits(path: Path) -> int:
    """
    Return the traditional rwx permission bits (0o000-0o777) for *path*.
    """
    return path.stat().st_mode & 0o777


def _human_mode(mode: int) -> str:
    """
    Return the mode as a 4-digit zero-padded octal string (e.g. '0755').
    """
    return f"{mode:04o}"


@pytest.fixture(scope="module")
def audit_contents():
    """
    Provide a dictionary {basename: Path} for all entries that exist
    directly under /home/user/audit_sample.
    """
    if not AUDIT_DIR.exists():
        pytest.fail(f"Required directory {AUDIT_DIR} is missing")

    if not AUDIT_DIR.is_dir():
        pytest.fail(f"{AUDIT_DIR} exists but is not a directory")

    return {p.name: p for p in AUDIT_DIR.iterdir()}


def test_expected_entries_present(audit_contents):
    """
    Verify that every expected file/directory is present.
    """
    for name in EXPECTED_ENTRIES:
        assert (
            name in audit_contents
        ), f"Missing expected entry: {AUDIT_DIR / name!s}"


def test_no_unexpected_entries(audit_contents):
    """
    Ensure there are no extra entries beyond the four that are expected.
    """
    unexpected = sorted(set(audit_contents) - set(EXPECTED_ENTRIES))
    assert (
        not unexpected
    ), (
        "Found unexpected entries inside "
        f"{AUDIT_DIR}: {', '.join(unexpected)}"
    )


@pytest.mark.parametrize("name, props", EXPECTED_ENTRIES.items())
def test_entry_type_and_permissions(audit_contents, name, props):
    """
    For each expected entry, assert correct type and permission bits.
    """
    expected_type, expected_mode = props
    path = audit_contents.get(name)

    # Sanity: existence already checked in previous test
    assert path is not None, "Internal test error: path is None"

    if expected_type == "file":
        assert path.is_file(), f"{path} should be a regular file"
    elif expected_type == "dir":
        assert path.is_dir(), f"{path} should be a directory"
    else:
        pytest.fail(f"Unknown expected type '{expected_type}' for {name}")

    actual_mode = _mode_bits(path)
    assert (
        actual_mode == expected_mode
    ), (
        f"Incorrect permissions on {path}: expected "
        f"{_human_mode(expected_mode)}, got {_human_mode(actual_mode)}"
    )