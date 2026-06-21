# test_initial_state.py
#
# Pytest suite that verifies the initial on-disk state *before* the student
# script is executed.  It checks that the solver repository exists, has the
# correct permissions, contains exactly the expected artefacts and that every
# artefact has the correct size.  Failures explicitly describe the mismatch.
#
# NOTE:  Per the exercise specification we intentionally do **not** test for the
#        presence or absence of any result files under /home/user/reports.
#
# Only Python’s stdlib and pytest are used.

import os
import re
import stat
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Constant reference data derived from the exercise description
# --------------------------------------------------------------------------- #

REPO_DIR = Path("/home/user/repos/solvers")
EXPECTED_ARTEFACTS = {
    "glpk-5.0-linux-x86_64.tar.gz": 1536000,
    "glpk-5.1-linux-x86_64.tar.gz": 1658880,
    "cplex-12.10-linux-x86_64.bin": 307200000,
    "cplex-22.1-linux-x86_64.bin": 319979520,
    "gurobi-9.1.1-linux-x86_64.tar.gz": 286720000,
    "gurobi-10.0.0-linux-x86_64.tar.gz": 325058560,
}

# Strict filename pattern as stated in task description
FILENAME_RE = re.compile(
    r"""
    ^
    (?P<name>[a-z]+)-                      # solver name, lowercase, no dashes
    (?P<version>[0-9]+\.[0-9]+(?:\.[0-9]+)?) # version MAJOR.MINOR(.PATCH)
    -linux-x86_64\.
    (?P<ext>(?:tar\.gz|bin))               # archive extension
    $
    """,
    re.VERBOSE,
)


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #


def _mode(path: Path) -> int:
    """Return the permission bits of `path` as an octal integer, e.g. 0o755."""
    return stat.S_IMODE(path.stat().st_mode)


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #


def test_repository_directory_exists_and_permissions():
    assert REPO_DIR.exists(), f"Expected {REPO_DIR} to exist."
    assert REPO_DIR.is_dir(), f"Expected {REPO_DIR} to be a directory."

    mode = _mode(REPO_DIR)
    assert (
        mode == 0o755
    ), f"Expected {REPO_DIR} to have mode 755 but it is {oct(mode)}."


def test_repository_contains_exact_expected_files():
    actual_files = {p.name for p in REPO_DIR.iterdir() if p.is_file()}
    expected_files = set(EXPECTED_ARTEFACTS.keys())

    missing = expected_files - actual_files
    extra = actual_files - expected_files

    assert not missing, (
        f"The following expected files are missing from {REPO_DIR}: "
        f"{', '.join(sorted(missing))}"
    )
    assert not extra, (
        f"The repository contains unexpected files that are not part of the "
        f"initial state: {', '.join(sorted(extra))}"
    )


@pytest.mark.parametrize("filename,expected_size", EXPECTED_ARTEFACTS.items())
def test_each_expected_file_has_correct_size(filename, expected_size):
    path = REPO_DIR / filename
    assert path.exists(), f"Missing expected file {path}"
    actual_size = path.stat().st_size
    assert (
        actual_size == expected_size
    ), f"{filename} size mismatch: expected {expected_size} bytes, got {actual_size} bytes"


@pytest.mark.parametrize("filename", EXPECTED_ARTEFACTS.keys())
def test_filenames_conform_to_pattern(filename):
    assert FILENAME_RE.match(
        filename
    ), f"Filename {filename} does not match required pattern '<name>-<version>-linux-x86_64.<ext>'"