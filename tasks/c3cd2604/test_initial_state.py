# test_initial_state.py
"""
Pytest suite that validates the *initial* filesystem state **before** the
student starts working on the “symlink clean-up” exercise.

It asserts that:
1. The expected source CSV files are present.
2. The “links” directory contains exactly the two specified symlinks
   (one of which is intentionally broken).
3. The “clean_links” directory and audit log do *not* exist yet.
4. The old_sales symlink is broken, while cust_link resolves correctly.

If any check fails, the corresponding assertion message should tell the
learner exactly what is wrong.
"""

import os
from pathlib import Path
import pytest

HOME = Path("/home/user")
PROJECTS = HOME / "projects"
DATASETS = PROJECTS / "datasets"
RAW_DIR = DATASETS / "raw"
LINKS_DIR = DATASETS / "links"
CLEAN_DIR = DATASETS / "clean_links"
AUDIT_LOG = PROJECTS / "link_audit.log"

RAW_FILES = {
    "sales_2020.csv",
    "sales_2021.csv",
    "customers_2020.csv",
}

SYMLINKS_EXPECTED = {
    "old_sales": "../raw/sales_2019.csv",           # broken target
    "cust_link": "../raw/customers_2020.csv",       # valid target
}


@pytest.fixture(scope="module")
def raw_contents():
    """Return a dictionary mapping filename -> Path for the raw directory."""
    assert RAW_DIR.is_dir(), (
        f"Required directory {RAW_DIR} is missing. "
        "It must already exist and contain the CSV files."
    )
    return {p.name: p for p in RAW_DIR.iterdir() if p.is_file() or p.is_symlink()}


def test_raw_directory_has_exactly_three_regular_csv_files(raw_contents):
    # Ensure the set of raw files is exactly what is expected
    found = set(raw_contents)
    assert found == RAW_FILES, (
        f"{RAW_DIR} must contain exactly these files: {sorted(RAW_FILES)}; "
        f"found: {sorted(found)}"
    )

    # Make sure each is a regular file (not a symlink)
    for name in RAW_FILES:
        p = raw_contents[name]
        assert p.is_file() and not p.is_symlink(), (
            f"{p} must be a regular file, not a symlink."
        )


def test_links_directory_structure():
    # Directory exists
    assert LINKS_DIR.is_dir(), (
        f"Required directory {LINKS_DIR} is missing. "
        "It must exist with the two initial symlinks."
    )

    # Collect entries
    dir_entries = {p.name: p for p in LINKS_DIR.iterdir()}
    found_names = set(dir_entries)
    expected_names = set(SYMLINKS_EXPECTED)
    assert found_names == expected_names, (
        f"{LINKS_DIR} must contain exactly these two entries: "
        f"{sorted(expected_names)}; found: {sorted(found_names)}."
    )

    # Validate individual symlinks
    for name, expected_link_text in SYMLINKS_EXPECTED.items():
        path = dir_entries[name]
        assert path.is_symlink(), f"{path} must be a symbolic link."

        # The raw link text must match exactly
        actual_text = os.readlink(path)
        assert actual_text == expected_link_text, (
            f"Symlink {path} should point to '{expected_link_text}', "
            f"but actually points to '{actual_text}'."
        )

        # Determine whether the link should be broken or valid
        resolved = (path.parent / actual_text).resolve()
        if name == "old_sales":
            assert not resolved.exists(), (
                f"{path} is supposed to be a *broken* symlink, but "
                f"its resolved target {resolved} unexpectedly exists."
            )
        else:  # cust_link
            assert resolved.exists() and resolved.is_file(), (
                f"{path} should resolve to existing file {resolved}, "
                "but it does not."
            )


def test_clean_links_directory_does_not_exist_yet():
    assert not CLEAN_DIR.exists(), (
        f"{CLEAN_DIR} should NOT exist before the student starts. "
        "It will be created as part of the task."
    )


def test_audit_log_not_present():
    assert not AUDIT_LOG.exists(), (
        f"{AUDIT_LOG} should NOT exist before the task is carried out."
    )