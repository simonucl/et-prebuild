# test_initial_state.py
#
# This pytest suite validates the OPERATING SYSTEM / FILE-SYSTEM *before*
# the student performs any actions.  It asserts the presence and integrity of
# the provisioning log that the student is expected to read and summarise.
#
# ──────────────────────────────────────────────────────────────────────────
# What we deliberately DO NOT test:
#   • /home/user/output            (must be created by the student later)
#   • /home/user/output/*.txt      (same reason as above)
#
# Only the *pre-existing* artifacts are checked here.

import re
from pathlib import Path

import pytest

LOG_PATH = Path("/home/user/logs/provisioning.log")

#: Regular expression for a single log line:
#:   YYYY-MM-DDTHH:MM:SSZ <LEVEL> <MESSAGE>
LOG_LINE_REGEX = re.compile(
    r"""
    ^                           # start of line
    \d{4}-\d{2}-\d{2}T          # YYYY-MM-DDT
    \d{2}:\d{2}:\d{2}Z          # HH:MM:SSZ
    \s+
    (INFO|ERROR|WARN|DEBUG)     # log level
    \s+
    .+                          # the rest of the message
    $                           # end of line
    """,
    re.VERBOSE,
)

# ---------------------------------------------------------------------------


def test_log_file_exists_and_is_readable():
    """
    The provisioning log must exist *before* the student runs any commands.
    """
    assert LOG_PATH.exists(), (
        f"Expected log file at {LOG_PATH} to exist, but it is missing."
    )
    assert LOG_PATH.is_file(), (
        f"Expected {LOG_PATH} to be a regular file, but it is not."
    )
    try:
        LOG_PATH.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Log file {LOG_PATH} is not readable: {exc}")


def test_all_log_lines_match_required_format():
    """
    Every line in the log file must follow the schema:
        YYYY-MM-DDTHH:MM:SSZ <LEVEL> <MESSAGE>
    """
    bad_lines = []
    for lineno, line in enumerate(LOG_PATH.read_text(encoding="utf-8").splitlines(), 1):
        if not LOG_LINE_REGEX.match(line):
            bad_lines.append((lineno, line))

    assert not bad_lines, (
        "Some lines do not match the required format:\n"
        + "\n".join(f"Line {ln}: {content!r}" for ln, content in bad_lines)
    )


def test_success_indicator_count_is_three():
    """
    The ground-truth count of successful provisions is *exactly three*.
    This value will later be compared against the student's output.
    """
    success_lines = [
        line
        for line in LOG_PATH.read_text(encoding="utf-8").splitlines()
        if "Provisioning succeeded:" in line
    ]
    assert len(
        success_lines
    ) == 3, (
        f"Expected exactly 3 lines containing 'Provisioning succeeded:' "
        f"but found {len(success_lines)}."
    )