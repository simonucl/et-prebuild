# test_initial_state.py
#
# This pytest module verifies that the operating-system state **before**
# the student starts their task is correct.
#
# What we DO test for:
#   • Presence of the source HTML log file.
#   • Basic sanity of its contents (it must contain the expected
#     “status:FAIL” lines for users bob and carol in that order).
#
# What we explicitly do NOT test for:
#   • Presence (or absence) of /home/user/analysis or any output files.
#
# Only stdlib and pytest are used.

import re
from pathlib import Path

SOURCE_LOG = Path("/home/user/data/access-log.html")


def _get_log_text() -> str:
    """Return the full text of the HTML log file."""
    try:
        return SOURCE_LOG.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise AssertionError(
            f"Required log file {SOURCE_LOG} is missing. "
            "Make sure the file is present before running the exercise."
        ) from exc


def test_access_log_file_exists():
    """Verify that the source HTML log file is present and is a regular file."""
    assert SOURCE_LOG.exists(), (
        f"Expected source file {SOURCE_LOG} to exist, but it does not."
    )
    assert SOURCE_LOG.is_file(), (
        f"Expected {SOURCE_LOG} to be a regular file, "
        f"but found a different kind of filesystem object."
    )


def test_access_log_contains_expected_fail_lines():
    """
    The HTML must already contain two failed-login lines for:
        • bob
        • carol
    in that order, each ending with the literal string 'status:FAIL'.
    """
    text = _get_log_text()

    # Extract lines within the <pre id="log"> … </pre> block for robustness.
    pre_block_match = re.search(r"<pre[^>]*>(.*?)</pre>", text, re.DOTALL | re.IGNORECASE)
    assert pre_block_match, (
        "The log HTML must contain a <pre id=\"log\"> … </pre> block with the events."
    )
    log_lines = pre_block_match.group(1).strip().splitlines()

    # Collect the lines whose last field is exactly 'status:FAIL'.
    fail_lines = [
        line for line in log_lines
        if re.search(r"\bstatus:FAIL\s*$", line)
    ]

    assert fail_lines, (
        "No lines ending with 'status:FAIL' were found in the log; "
        "at least two such lines (for bob and carol) are expected."
    )

    # Verify that the FAIL lines are exactly for bob and carol, in order.
    expected_users = ["bob", "carol"]
    extracted_users = []
    user_pattern = re.compile(r"user:([a-zA-Z0-9_]+)\s+-\s+status:FAIL\s*$")

    for line in fail_lines:
        match = user_pattern.search(line)
        assert match, (
            f"FAIL line does not match expected pattern 'user:<name> - status:FAIL':\n{line}"
        )
        extracted_users.append(match.group(1))

    assert extracted_users == expected_users, (
        "FAIL lines do not match expected users and/or order.\n"
        f"Expected order : {expected_users}\n"
        f"Found order    : {extracted_users}"
    )