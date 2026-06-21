# test_initial_state.py
#
# This pytest suite validates the **initial** state of the operating-system /
# file-system before the student performs any action.  It purposefully does
# NOT test for the presence of any files that are expected to be created by
# the student (see the rubric).  If any check below fails, the accompanying
# assertion message will precisely describe what is missing or out of place.
#
# Requirements verified:
#   • /home/user/hardening   -> must exist and be a directory (0755)
#   • /home/user/hardening/tuned.conf -> must exist and be a regular file
#     with permission bits 0644
#   • The contents of tuned.conf must be **exactly** the five-line snippet
#     provided in the task description, including the final trailing newline.
#
# Only the Python standard library and pytest are used.

import os
import stat
import pytest
from pathlib import Path

HARDENING_DIR = Path("/home/user/hardening")
TUNED_CONF = HARDENING_DIR / "tuned.conf"

# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _mode_bits(path: Path) -> int:
    """
    Return the permission bits (e.g. 0o755) for the given filesystem path.
    """
    return stat.S_IMODE(path.stat().st_mode)


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_hardening_directory_exists_and_has_correct_mode():
    assert HARDENING_DIR.exists(), (
        f"Required directory {HARDENING_DIR} does not exist."
    )
    assert HARDENING_DIR.is_dir(), (
        f"{HARDENING_DIR} exists but is not a directory."
    )

    expected_mode = 0o755
    actual_mode = _mode_bits(HARDENING_DIR)
    assert actual_mode == expected_mode, (
        f"{HARDENING_DIR} has permissions {oct(actual_mode)}, "
        f"expected {oct(expected_mode)}."
    )


def test_tuned_conf_exists_and_has_correct_mode_and_content():
    # ---- existence & mode -------------------------------------------------- #
    assert TUNED_CONF.exists(), (
        f"Expected file {TUNED_CONF} is missing."
    )
    assert TUNED_CONF.is_file(), (
        f"{TUNED_CONF} exists but is not a regular file."
    )

    expected_mode = 0o644
    actual_mode = _mode_bits(TUNED_CONF)
    assert actual_mode == expected_mode, (
        f"{TUNED_CONF} has permissions {oct(actual_mode)}, "
        f"expected {oct(expected_mode)}."
    )

    # ---- exact content ----------------------------------------------------- #
    expected_content = (
        "# Kernel scheduler settings\n"
        "sched_migration_cost_ns = 500000\n"
        "sched_latency_ns = 6000000\n"
        "sched_min_granularity_ns = 750000\n"
        "# end\n"
    )

    with TUNED_CONF.open("r", encoding="utf-8") as fh:
        actual_content = fh.read()

    # Provide detailed diff if the file differs
    assert actual_content == expected_content, (
        f"The contents of {TUNED_CONF} do not match the expected initial "
        "state.  If you have already modified the file, please revert it to "
        "the exact form shown in the task description before running the "
        "single-command solution."
    )