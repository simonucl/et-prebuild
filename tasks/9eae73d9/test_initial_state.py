# test_initial_state.py
#
# Pytest suite that validates the initial filesystem state *before* the student
# carries out any task.  All checks are performed with absolute paths and use
# only the Python standard library plus pytest.  Any failure message should
# make it immediately clear what is wrong or missing.

from pathlib import Path
import pytest

ROOT = Path("/home/user/site_admin")


def _read_file_lines(path: Path):
    """
    Helper to read all lines of a text file, preserving newline characters.
    """
    with path.open("r", encoding="utf-8") as fh:
        return fh.readlines()


def test_root_directory_exists():
    """Ensure the main site_admin directory is present."""
    assert ROOT.is_dir(), f"Required directory {ROOT} is missing."


def test_new_hires_csv_has_only_header():
    """
    /home/user/site_admin/new_hires.csv must exist and contain exactly ONE line,
    the header: 'username,uid,group,shell,home_dir,required_packages\\n'
    """
    csv_path = ROOT / "new_hires.csv"
    assert csv_path.is_file(), f"Missing file: {csv_path}"

    lines = _read_file_lines(csv_path)
    expected_header = "username,uid,group,shell,home_dir,required_packages\n"

    assert lines == [expected_header], (
        f"{csv_path} should contain exactly one header line:\n"
        f"  {expected_header!r}\n"
        f"Current content ({len(lines)} lines):\n{''.join(lines)!r}"
    )


def test_packages_database_contents():
    """
    Verify that packages_database.txt exists and contains exactly the five
    expected lines (with trailing newlines).
    """
    db_path = ROOT / "packages_database.txt"
    assert db_path.is_file(), f"Missing file: {db_path}"

    lines = _read_file_lines(db_path)
    expected_lines = [
        "bash,5.1-2\n",
        "coreutils,8.32-4\n",
        "nano,5.4-2\n",
        "curl,7.74.0-1\n",
        "python3,3.9.2-1\n",
    ]

    assert lines == expected_lines, (
        f"{db_path} contents do not match the expected inventory.\n"
        f"Expected:\n{''.join(expected_lines)!r}\n"
        f"Found:\n{''.join(lines)!r}"
    )


def test_users_directory_exists_and_is_empty():
    """
    /home/user/site_admin/users/ must exist and be empty.
    """
    users_dir = ROOT / "users"
    assert users_dir.is_dir(), f"Missing directory: {users_dir}"

    contents = list(users_dir.iterdir())
    assert contents == [], (
        f"{users_dir} is expected to be empty but contains: "
        f"{', '.join(str(p) for p in contents)}"
    )


def test_no_user_subdirectories_precreated():
    """
    Ensure that alice and bob directories do not pre-exist within users/.
    This is a more explicit check in case the previous test is relaxed later.
    """
    for name in ("alice", "bob"):
        path = ROOT / "users" / name
        assert not path.exists(), f"Directory {path} should NOT exist yet."


def test_package_audit_log_not_present_initially():
    """
    The package_audit.log file must *not* exist prior to the student's work.
    """
    audit_log = ROOT / "package_audit.log"
    assert not audit_log.exists(), (
        f"Unexpected file {audit_log} already exists; it should be created by "
        "the student's solution, not beforehand."
    )