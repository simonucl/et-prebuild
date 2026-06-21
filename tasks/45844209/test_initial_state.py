# test_initial_state.py
#
# Pytest suite to validate the expected **initial** filesystem state
# before the student modifies anything.
#
# • Verifies that /home/user/ci_cd exists and has the correct permissions.
# • Verifies that /home/user/ci_cd/build_stats.csv exists, is readable,
#   has the expected permissions, and its exact expected contents.
# • Ensures that the yet-to-be-created output file
#   /home/user/ci_cd/build_stats_compact.csv is NOT present.
#
# Only Python stdlib and pytest are used.

import os
import stat
import textwrap
import pytest

CI_CD_DIR = "/home/user/ci_cd"
SOURCE_FILE = os.path.join(CI_CD_DIR, "build_stats.csv")
OUTPUT_FILE = os.path.join(CI_CD_DIR, "build_stats_compact.csv")


@pytest.fixture(scope="module")
def expected_source_lines():
    """
    Returns the exact list of lines (with trailing newlines) that should be
    present in /home/user/ci_cd/build_stats.csv in the initial state.
    """
    csv_text = textwrap.dedent(
        """\
        BuildID,Branch,CommitHash,Author,Status,DurationSec,ArtifactsSizeMB,Timestamp
        101,main,ab12cd3,alice,success,245,120,2023-08-23T10:15:31Z
        102,develop,bc34de5,bob,failed,130,0,2023-08-23T10:20:12Z
        103,main,cd56ef7,charlie,success,300,98,2023-08-23T10:50:45Z
        104,hotfix,ef78gh9,dana,success,210,110,2023-08-23T11:15:02Z
        """
    )
    # Ensure each line (including last) ends with a single '\n'
    return [line + "\n" for line in csv_text.splitlines()]


def _mode_as_octal(path):
    """Helper to return the permission bits of a file/directory in octal (e.g., 0o755)."""
    return stat.S_IMODE(os.stat(path).st_mode)


def test_ci_cd_directory_exists():
    assert os.path.isdir(CI_CD_DIR), (
        f"Required directory {CI_CD_DIR!r} is missing. "
        "It should exist with permissions 0755."
    )
    actual_mode = _mode_as_octal(CI_CD_DIR)
    expected_mode = 0o755
    assert actual_mode == expected_mode, (
        f"{CI_CD_DIR!r} exists but has permissions {oct(actual_mode)}; "
        f"expected {oct(expected_mode)} (rwxr-xr-x)."
    )


def test_source_csv_exists_and_permissions():
    assert os.path.isfile(SOURCE_FILE), (
        f"Source CSV file {SOURCE_FILE!r} is missing. "
        "It should exist before the student begins."
    )
    actual_mode = _mode_as_octal(SOURCE_FILE)
    expected_mode = 0o644
    assert actual_mode == expected_mode, (
        f"{SOURCE_FILE!r} exists but has permissions {oct(actual_mode)}; "
        f"expected {oct(expected_mode)} (rw-r--r--)."
    )


def test_source_csv_contents(expected_source_lines):
    # Read the file in text mode with UTF-8 encoding
    with open(SOURCE_FILE, "r", encoding="utf-8") as fh:
        content = fh.read()

    # The file must end with a single newline character
    assert content.endswith("\n"), (
        f"{SOURCE_FILE!r} must end with a single Unix newline '\\n'."
    )

    # Split into lines (keeping trailing '\n')
    lines = content.splitlines(keepends=True)

    # Ensure no extra blank lines
    assert lines[-1] != "\n", (
        f"{SOURCE_FILE!r} contains an unexpected blank line at the end."
    )

    # Verify the exact expected lines
    assert lines == expected_source_lines, (
        f"Contents of {SOURCE_FILE!r} do not match the expected initial dataset.\n"
        "Expected lines:\n"
        + "".join(expected_source_lines)
        + "\nActual lines:\n"
        + "".join(lines)
    )


def test_output_file_does_not_exist_initially():
    assert not os.path.exists(OUTPUT_FILE), (
        f"Output file {OUTPUT_FILE!r} already exists before the student has run "
        "their solution. The repository should start without this file."
    )