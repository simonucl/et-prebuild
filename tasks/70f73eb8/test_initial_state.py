# test_initial_state.py
#
# This pytest file validates **the initial state** of the filesystem
# before the student runs any commands for the “disk-utilisation
# summary” exercise.  It checks that the raw report is present with the
# exact expected contents and that no output artefacts created by the
# student exist yet.

import os
import stat
import pytest

HOME = "/home/user"
DISK_DIR = os.path.join(HOME, "disk_usage")
FULL_REPORT = os.path.join(DISK_DIR, "full_report.tsv")
SUMMARY = os.path.join(DISK_DIR, "disk_summary.tsv")
ACTION_LOG = os.path.join(DISK_DIR, "actions.log")

EXPECTED_FULL_REPORT = (
    "Server\tMount\tTotal_GB\tUsed_GB\tFree_GB\tUse_percent\n"
    "srv1\t/\t500\t350\t150\t70%\n"
    "srv2\t/\t1000\t600\t400\t60%\n"
    "srv3\t/data\t2000\t1200\t800\t60%\n"
    "srv4\t/backup\t1500\t1200\t300\t80%\n"
)


def test_disk_usage_directory_exists_and_permissions():
    """The /home/user/disk_usage directory must exist and be accessible."""
    assert os.path.isdir(DISK_DIR), (
        f"Expected directory {DISK_DIR} to exist, but it is missing."
    )

    mode = stat.S_IMODE(os.stat(DISK_DIR).st_mode)
    # Owner must have rwx (0o700), group/others must have at least rx (0o005)
    owner_perms = mode & 0o700
    group_other_perms = mode & 0o077
    assert owner_perms == 0o700, (
        f"{DISK_DIR} should have rwx permissions for the owner "
        f"(700), but has {oct(mode)}."
    )
    # Group and others need read/execute; we accept 5 (rx) or 0
    for scope, mask in [("group", 0o070), ("others", 0o007)]:
        perms = mode & mask
        acceptable = {0, 0o050, 0o070, 0o005, 0o007}
        assert perms in acceptable, (
            f"{DISK_DIR} should allow at most read/execute for {scope}; "
            f"found permissions {oct(mode)}."
        )


def test_only_full_report_is_present_initially():
    """
    Initially, only 'full_report.tsv' should exist in /home/user/disk_usage.
    'disk_summary.tsv' and 'actions.log' must NOT exist yet.
    """
    # Collect visible (non-dot) files/directories for clarity.
    visible_items = [f for f in os.listdir(DISK_DIR) if not f.startswith(".")]
    assert visible_items == ["full_report.tsv"], (
        "Before the student starts, the directory should contain ONLY "
        "'full_report.tsv'. Instead found: " + ", ".join(sorted(visible_items))
    )

    assert not os.path.exists(SUMMARY), (
        f"Output summary file {SUMMARY} should NOT exist before the task begins."
    )
    assert not os.path.exists(ACTION_LOG), (
        f"Log file {ACTION_LOG} should NOT exist before the task begins."
    )


def test_full_report_contents_exact_match():
    """Validate the exact bytes of full_report.tsv."""
    assert os.path.isfile(FULL_REPORT), (
        f"Expected raw report {FULL_REPORT} to exist, but it is missing."
    )

    with open(FULL_REPORT, "r", encoding="utf-8") as fp:
        content = fp.read()

    # Simple equality comparison gives pytest a nice diff on failure.
    assert content == EXPECTED_FULL_REPORT, (
        f"The contents of {FULL_REPORT} do not match the expected initial "
        f"report.\nExpected:\n{EXPECTED_FULL_REPORT!r}\n\nFound:\n{content!r}"
    )

    # Additional sanity checks on newline termination.
    assert content.endswith("\n"), (
        f"{FULL_REPORT} must terminate with exactly one newline character."
    )
    assert not content.endswith("\n\n"), (
        f"{FULL_REPORT} contains more than one trailing newline."
    )