# test_initial_state.py
#
# This pytest suite validates that the starting state of the filesystem
# matches the specification *before* the student begins any work.
#
# Rules respected:
#   • Uses only stdlib + pytest.
#   • Checks absolute paths.
#   • Does NOT touch or mention the to-be-generated artefacts
#     (warnings_summary.log, warnings_count.csv).
#   • Provides clear failure messages.

import os
from pathlib import Path

import pytest

# Absolute paths used throughout the tests
LOG_DIR = Path("/home/user/project/logs")
BUILD_LOG = LOG_DIR / "build.log"

# The build.log must contain the following 12 lines *exactly*,
# each terminated by a single '\n'.  The final line is also
# terminated by '\n', and there is no extra blank line afterwards.
EXPECTED_BUILD_LOG_LINES = [
    "2024-04-10 10:15:23 INFO  [INIT] : Starting build\n",
    "2024-04-10 10:15:25 WARNING [DOC-1001]: Deprecated tag <note> found in file intro.md\n",
    "2024-04-10 10:15:26 ERROR [DOC-9002]: Missing image intro.png referenced in intro.md\n",
    "2024-04-10 10:15:27 WARNING [DOC-1002]: Obsolete attribute \"align\" in file layout.html\n",
    "2024-04-10 10:15:28 INFO  [CHECK] : Spellcheck completed\n",
    "2024-04-10 10:15:29 WARNING [DOC-1001]: Deprecated tag <note> found in file usage.md\n",
    "2024-04-10 10:15:30 WARNING [DOC-1003]: Long line (>120 chars) in getting_started.rst:432\n",
    "2024-04-10 10:15:31 INFO  [BUILD] : Build step completed\n",
    "2024-04-10 10:15:32 WARNING [DOC-1002]: Obsolete attribute \"align\" in file legacy.html\n",
    "2024-04-10 10:15:33 WARNING [DOC-1004]: Internal link reference missing in api.md\n",
    "2024-04-10 10:15:34 ERROR [SYS-3001]: Unknown system error\n",
    "2024-04-10 10:15:35 INFO  [DONE] : Build finished\n",
]


@pytest.mark.dependency(name="dir_exists")
def test_logs_directory_exists():
    """The /home/user/project/logs directory must exist."""
    assert LOG_DIR.is_dir(), f"Expected directory {LOG_DIR} does not exist"


@pytest.mark.dependency(name="build_log_exists", depends=["dir_exists"])
def test_build_log_exists():
    """The build.log file must exist at the exact path specified."""
    assert BUILD_LOG.is_file(), f"Expected file {BUILD_LOG} does not exist"


@pytest.mark.dependency(depends=["build_log_exists"])
def test_build_log_contents():
    """
    build.log must match the canonical contents exactly:
      • 12 lines
      • Each line identical to the specification
      • File ends with a single trailing newline, no extra blank lines
    """
    with BUILD_LOG.open("r", encoding="utf-8") as fh:
        data = fh.read()

    # Ensure file ends with exactly one newline and not more
    assert data.endswith(
        "\n"
    ), "build.log must end with a single trailing newline"
    assert not data.endswith(
        "\n\n"
    ), "build.log must not have more than one trailing newline"

    lines = data.splitlines(keepends=True)

    # Validate line count
    assert len(lines) == len(
        EXPECTED_BUILD_LOG_LINES
    ), f"build.log should have {len(EXPECTED_BUILD_LOG_LINES)} lines, found {len(lines)}"

    # Compare each line verbatim
    for idx, (actual, expected) in enumerate(
        zip(lines, EXPECTED_BUILD_LOG_LINES), start=1
    ):
        assert (
            actual == expected
        ), f"Line {idx} mismatch.\nExpected: {expected!r}\nFound   : {actual!r}"