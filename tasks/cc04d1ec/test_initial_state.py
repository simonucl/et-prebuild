# test_initial_state.py
#
# Pytest suite that validates the machine’s initial state **before**
# the student performs any action for the “environment manifest” task.
#
# This file checks ONLY the pre-existing reference artefacts; it does
# not (and must not) check for the /home/user/backup directory or the
# env_20240615.log file that the student will create later.

import pathlib
import pytest

HOME = pathlib.Path("/home/user")
SYSTEM_INFO_DIR = HOME / "system_info"
TIMEZONE_FILE = SYSTEM_INFO_DIR / "timezone.conf"
LOCALE_FILE = SYSTEM_INFO_DIR / "locale.conf"

EXPECTED_TIMEZONE_CONTENT = "Etc/UTC\n"
EXPECTED_LOCALE_CONTENT = "en_US.UTF-8\n"


def _assert_single_line_file(path: pathlib.Path, expected_content: str) -> None:
    """
    Helper that asserts:
      • path exists and is a regular file
      • file content matches expected_content exactly
      • file contains exactly one newline character, which must be the final byte
    """
    assert path.exists(), f"Required file is missing: {path}"
    assert path.is_file(), f"Expected a regular file at {path}, but found something else."

    data = path.read_text(encoding="utf-8")
    msg_prefix = f"File {path} must contain exactly the expected line."

    # Exact byte-for-byte content check
    assert (
        data == expected_content
    ), (
        f"{msg_prefix}\n"
        f"Expected: {repr(expected_content)}\n"
        f"Found:    {repr(data)}"
    )

    # Additional explicit structural checks for clarity
    newline_count = data.count("\n")
    assert newline_count == 1, (
        f"{msg_prefix} It should end with a single newline. "
        f"Found {newline_count} newline character(s)."
    )
    assert data.endswith("\n"), f"{msg_prefix} Must end with a single newline character."


@pytest.mark.describe("Pre-existing reference files must be present and correct")
class TestInitialState:
    def test_timezone_conf_exists_and_is_correct(self):
        """
        /home/user/system_info/timezone.conf must exist and contain:
        'Etc/UTC\\n'
        """
        _assert_single_line_file(TIMEZONE_FILE, EXPECTED_TIMEZONE_CONTENT)

    def test_locale_conf_exists_and_is_correct(self):
        """
        /home/user/system_info/locale.conf must exist and contain:
        'en_US.UTF-8\\n'
        """
        _assert_single_line_file(LOCALE_FILE, EXPECTED_LOCALE_CONTENT)