# test_initial_state.py
"""
Pytest suite that validates the **initial** operating-system / filesystem
state before the student performs any action for the “firewall manifest” task.

What we assert (truth values for the fresh workspace):

1. /home/user/etl_firewall_rules.conf
   • The file **exists**.
   • It contains **exactly one line**:
       "# ETL Pipeline Firewall Rules\n"
     (i.e. a trailing newline is present, and there are no extra lines.)

2. /home/user/etl_firewall_apply.log
   • The file **must NOT exist yet**.

If any assertion fails, the error message explains what is wrong so the
student can understand why the initial state is unexpected.
"""

from pathlib import Path
import pytest

RULES_PATH = Path("/home/user/etl_firewall_rules.conf")
LOG_PATH = Path("/home/user/etl_firewall_apply.log")
EXPECTED_FIRST_LINE = "# ETL Pipeline Firewall Rules\n"


@pytest.fixture(scope="module")
def rules_contents():
    """
    Return the text contents of /home/user/etl_firewall_rules.conf.

    The fixture asserts early that the file exists so that later tests can rely
    on its presence without redundant existence checks.
    """
    if not RULES_PATH.exists():
        pytest.fail(
            f"Required file is missing: {RULES_PATH}\n"
            "The initial workspace must already contain this manifest."
        )
    if not RULES_PATH.is_file():
        pytest.fail(
            f"{RULES_PATH} exists but is not a regular file."
        )
    try:
        return RULES_PATH.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read {RULES_PATH}: {exc}")  # noqa: TRY003


def test_rules_file_has_only_the_expected_first_line(rules_contents):
    """
    Ensure the firewall rules manifest starts with exactly the provided comment
    line and *nothing else*.
    """
    assert (
        rules_contents == EXPECTED_FIRST_LINE
    ), (
        f"{RULES_PATH} should contain exactly one line:\n"
        f"    {EXPECTED_FIRST_LINE!r}\n"
        f"but its actual contents were:\n"
        f"    {rules_contents!r}"
    )


def test_rules_file_has_single_line(rules_contents):
    """
    Redundant but explicit check that there is precisely one newline-terminated
    line (guards against accidental missing or extra newlines).
    """
    lines = rules_contents.splitlines(keepends=True)
    assert len(lines) == 1, (
        f"{RULES_PATH} is expected to have 1 line, found {len(lines)} lines."
    )


def test_apply_log_does_not_exist_yet():
    """
    The apply log should *not* exist before the student runs their commands.
    """
    assert not LOG_PATH.exists(), (
        f"The log file {LOG_PATH} should NOT exist before any rule is applied, "
        "but it is present in the initial workspace."
    )