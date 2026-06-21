# test_initial_state.py
#
# Pytest suite that verifies the pristine state of the workstation
# BEFORE the student starts working on the “SSH key-pair + CSV aggregation” task.
#
# These tests **must** pass on the unmodified machine.  If they fail,
# the testing environment itself is wrong.

import os
import stat
from pathlib import Path

HOME = Path("/home/user")

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def _mode(path: Path) -> int:
    """
    Return a file's permission bits as an int comparable to Unix octal
    notation (e.g. 0o644).  Symlinks are resolved.
    """
    return stat.S_IMODE(path.stat().st_mode)


def _assert_exists(path: Path, is_dir=False, expected_mode=None):
    if not path.exists():
        typ = "directory" if is_dir else "file"
        pytest.fail(f"Expected {typ} {path} to exist, but it does not.")
    if is_dir and not path.is_dir():
        pytest.fail(f"Expected {path} to be a directory, but it is not.")
    if not is_dir and not path.is_file():
        pytest.fail(f"Expected {path} to be a file, but it is not.")
    if expected_mode is not None:
        actual = _mode(path)
        if actual != expected_mode:
            pytest.fail(
                f"{path} has mode {oct(actual)}, expected {oct(expected_mode)}."
            )


def _assert_not_exists(path: Path):
    if path.exists():
        pytest.fail(f"{path} should NOT exist before the student runs their commands.")


# ---------------------------------------------------------------------------
# 1. Directories that must pre-exist
# ---------------------------------------------------------------------------


def test_required_directories_exist_with_correct_permissions():
    dirs_expected = {
        HOME / ".ssh": 0o700,
        HOME / "datasets": 0o755,
        HOME / "outputs": 0o755,
        HOME / "server_access": 0o700,
    }

    for path, mode in dirs_expected.items():
        _assert_exists(path, is_dir=True, expected_mode=mode)


# ---------------------------------------------------------------------------
# 2. Input CSV files (content + permissions)
# ---------------------------------------------------------------------------


def _read_text(path: Path) -> str:
    with path.open(encoding="utf-8") as f:
        return f.read()


def test_input_csv_files_are_intact():
    csv1 = HOME / "datasets" / "sales_q1.csv"
    csv2 = HOME / "datasets" / "sales_q2.csv"

    expected_content_q1 = (
        "Category,Revenue\n"
        "A,100\n"
        "B,150\n"
        "C,200\n"
    )
    expected_content_q2 = (
        "Category,Revenue\n"
        "A,120\n"
        "B,130\n"
        "D,90\n"
    )

    for csv, expected in [(csv1, expected_content_q1), (csv2, expected_content_q2)]:
        _assert_exists(csv, is_dir=False, expected_mode=0o644)
        actual = _read_text(csv)
        assert (
            actual == expected
        ), f"File {csv} content mismatch.\nExpected:\n{expected!r}\nGot:\n{actual!r}"


# ---------------------------------------------------------------------------
# 3. Pre-existing authorized_keys_data file
# ---------------------------------------------------------------------------


def test_authorized_keys_contains_single_dummy_key():
    auth_file = HOME / "server_access" / "authorized_keys_data"
    _assert_exists(auth_file, is_dir=False, expected_mode=0o600)

    lines = _read_text(auth_file).splitlines()
    assert (
        len(lines) >= 1
    ), f"{auth_file} should contain at least one line, found empty file."

    first_line = lines[0]
    assert first_line.startswith(
        "ssh-ed25519 "
    ), f"First line of {auth_file} should start with 'ssh-ed25519 '."


# ---------------------------------------------------------------------------
# 4. Files that must NOT exist yet
# ---------------------------------------------------------------------------


def test_output_and_key_files_do_not_exist():
    paths_should_not_exist = [
        HOME / ".ssh" / "id_ed25519_data",
        HOME / ".ssh" / "id_ed25519_data.pub",
        HOME / "outputs" / "key_fingerprint.txt",
        HOME / "outputs" / "agg_sales.csv",
        HOME / "outputs" / "process.log",
    ]

    for p in paths_should_not_exist:
        _assert_not_exists(p)