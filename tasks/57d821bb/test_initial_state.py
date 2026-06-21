# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state that must be present
# BEFORE the student executes any command for the “RPM pending updates” task.
#
# What we assert:
#   1. The directory /home/user/deployment/pending_updates exists and is a directory.
#   2. Exactly three “*.rpm” files are present in that directory.
#   3. Those three files are
#        • app-core-2.0.1.rpm
#        • db-driver-5.3.0.rpm
#        • ui-frontend-1.4.8.rpm
#
# We intentionally do NOT test anything about the expected output file
# (/home/user/deployment/update_summary.log) because the student hasn’t created
# it yet and the grading policy forbids asserting about output artefacts in the
# initial-state tests.

import os
from pathlib import Path

import pytest

PENDING_DIR = Path("/home/user/deployment/pending_updates")
EXPECTED_RPMS = {
    "app-core-2.0.1.rpm",
    "db-driver-5.3.0.rpm",
    "ui-frontend-1.4.8.rpm",
}


def test_pending_updates_directory_exists_and_is_dir():
    assert PENDING_DIR.exists(), (
        f"Required directory {PENDING_DIR} is missing. "
        "The deployment engineer relies on this folder being present."
    )
    assert PENDING_DIR.is_dir(), (
        f"{PENDING_DIR} exists but is not a directory. "
        "It must be a directory that can contain the RPM files."
    )


def test_expected_rpm_files_present_and_unique():
    # Collect only items that actually exist as files with '.rpm' extension.
    rpm_files_in_dir = {
        entry.name
        for entry in PENDING_DIR.iterdir()
        if entry.is_file() and entry.suffix == ".rpm"
    }

    # 1. All expected RPMs are present.
    missing = EXPECTED_RPMS - rpm_files_in_dir
    assert not missing, (
        "The following required RPM files are missing from "
        f"{PENDING_DIR}: {', '.join(sorted(missing))}"
    )

    # 2. No extra RPMs are lurking around.
    extra = rpm_files_in_dir - EXPECTED_RPMS
    assert not extra, (
        "Unexpected RPM files found in "
        f"{PENDING_DIR}: {', '.join(sorted(extra))}. "
        "The initial state should contain exactly the three specified packages."
    )

    # 3. Final sanity check: the directory holds exactly three RPM files.
    assert len(rpm_files_in_dir) == 3, (
        f"Expected exactly 3 RPM files in {PENDING_DIR}, "
        f"found {len(rpm_files_in_dir)}."
    )