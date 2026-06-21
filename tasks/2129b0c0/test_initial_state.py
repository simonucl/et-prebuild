# test_initial_state.py
#
# This pytest suite validates the **initial** filesystem state that must be
# present **before** the student begins the task.  It intentionally does *not*
# test for any of the output artefacts the student is expected to create
# (workspace directories, symlinks, audit log, etc.).
#
# The checks performed here are limited to the “given” portion of the task
# description—i.e. the two pre-existing application drops and their layout
# under /home/user/apps/.
#
# Only the Python standard library and pytest are used.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
APPS_DIR = HOME / "apps"

# Descriptions of the artifacts that MUST exist initially
ARTIFACTS = {
    "alpha_bin": APPS_DIR / "appAlpha-1.2" / "bin" / "alpha",
    "alpha_perf": APPS_DIR / "appAlpha-1.2" / "perfdata",
    "beta_bin": APPS_DIR / "appBeta-2.0" / "bin" / "beta",
    "beta_perf": APPS_DIR / "appBeta-2.0" / "perfdata",
}

# Expected file contents for the binaries (two lines each)
EXPECTED_CONTENTS = {
    ARTIFACTS["alpha_bin"]: ["#!/bin/bash", 'echo "Alpha v1.2"'],
    ARTIFACTS["beta_bin"]: ["#!/bin/bash", 'echo "Beta v2.0"'],
}


@pytest.mark.parametrize("path_key", ["alpha_bin", "beta_bin"])
def test_binaries_exist_and_have_expected_content(path_key):
    """
    Validate that each application binary exists, is a regular file,
    and contains exactly the two expected lines.
    """
    path = ARTIFACTS[path_key]
    assert path.exists(), f"Expected binary {path} does not exist."
    assert path.is_file(), f"Expected {path} to be a regular file."

    # Read and normalise line endings (strip trailing newlines/spaces)
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        lines = [ln.rstrip("\n\r") for ln in fh.readlines()]

    expected_lines = EXPECTED_CONTENTS[path]
    assert (
        lines == expected_lines
    ), f"Contents of {path} differ from expected.\nExpected: {expected_lines!r}\nFound:    {lines!r}"


@pytest.mark.parametrize("path_key", ["alpha_perf", "beta_perf"])
def test_perfdata_directories_exist_and_are_empty(path_key):
    """
    Validate that each perfdata directory exists, is a directory,
    and is initially empty.
    """
    path = ARTIFACTS[path_key]
    assert path.exists(), f"Expected directory {path} does not exist."
    assert path.is_dir(), f"Expected {path} to be a directory."

    # List directory; should be empty (no files or sub-dirs)
    contents = list(path.iterdir())
    assert (
        not contents
    ), f"Directory {path} is expected to be empty but contains: {[p.name for p in contents]}"


def test_apps_directory_structure_is_correct():
    """
    Sanity check that the overall apps directory exists and contains
    exactly the two expected application folders.
    """
    assert APPS_DIR.exists(), f"Expected base directory {APPS_DIR} does not exist."
    assert APPS_DIR.is_dir(), f"{APPS_DIR} should be a directory."

    expected_dirs = {"appAlpha-1.2", "appBeta-2.0"}
    found_dirs = {p.name for p in APPS_DIR.iterdir() if p.is_dir()}
    missing = expected_dirs - found_dirs
    extras = found_dirs - expected_dirs
    assert not missing, f"Missing expected application directories: {', '.join(sorted(missing))}"
    # Having extra dirs is usually benign, but we flag them to maintain a clean test environment.
    assert not extras, f"Unexpected directories found in {APPS_DIR}: {', '.join(sorted(extras))}"