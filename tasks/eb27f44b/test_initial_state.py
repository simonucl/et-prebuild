# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem state for the
# “largest-Python-packages” exercise.  These tests purposely look **only**
# at the resources that must already exist **before** the student starts
# working.  Nothing about the expected output artefacts is verified here.
#
# Rules recap (enforced below):
#   • /home/user/local_repo must exist and be a directory
#   • /home/user/local_repo/packages.tsv must exist, be readable and
#     follow the promised 3-column, TAB-separated format with positive
#     integer sizes and no header / comment lines.

import os
import pathlib
import pytest

REPO_DIR = pathlib.Path("/home/user/local_repo")
PKG_FILE = REPO_DIR / "packages.tsv"


def _read_packages_file():
    """
    Helper: returns list[str] of non-empty, stripped lines found in
    /home/user/local_repo/packages.tsv
    """
    with PKG_FILE.open("r", encoding="utf-8") as fh:
        # Strip trailing newline characters but **keep** internal tabs
        return [ln.rstrip("\n\r") for ln in fh if ln.strip()]


@pytest.mark.dependency()
def test_repo_directory_exists():
    assert REPO_DIR.exists(), (
        f"Required repository directory {REPO_DIR} is missing. "
        "The exercise cannot proceed without it."
    )
    assert REPO_DIR.is_dir(), (
        f"{REPO_DIR} exists but is not a directory: "
        "expected a directory containing packages.tsv."
    )


@pytest.mark.dependency(depends=["test_repo_directory_exists"])
def test_packages_file_exists_and_readable():
    assert PKG_FILE.exists(), (
        f"Expected file {PKG_FILE} is missing. "
        "It must be present before students start the task."
    )
    assert PKG_FILE.is_file(), (
        f"{PKG_FILE} exists but is not a regular file."
    )
    # Basic readability check
    try:
        _ = PKG_FILE.read_bytes()
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Unable to read {PKG_FILE}: {exc}")


@pytest.mark.dependency(depends=["test_packages_file_exists_and_readable"])
def test_packages_file_not_empty():
    lines = _read_packages_file()
    assert lines, f"{PKG_FILE} is empty; it must contain package data."


@pytest.mark.dependency(depends=["test_packages_file_exists_and_readable"])
def test_packages_file_tab_separated_and_three_columns():
    """
    Every non-blank line must contain exactly two TABs -> 3 columns:
      package <TAB> version <TAB> size_kib
    """
    bad_lines = []
    for i, line in enumerate(_read_packages_file(), start=1):
        tab_count = line.count("\t")
        if tab_count != 2:
            bad_lines.append((i, line, tab_count))

    assert not bad_lines, (
        "The following lines in packages.tsv do not have exactly three "
        "TAB-separated columns:\n"
        + "\n".join(
            f"  line {ln_num}: found {tabs} TAB(s) -> {ln_content!r}"
            for ln_num, ln_content, tabs in bad_lines
        )
    )


@pytest.mark.dependency(depends=["test_packages_file_tab_separated_and_three_columns"])
def test_size_column_positive_integer():
    """
    The third column (size_kib) must be a positive integer for every row.
    """
    violations = []
    for i, line in enumerate(_read_packages_file(), start=1):
        size_str = line.split("\t")[2]
        try:
            size_val = int(size_str)
            assert size_val > 0
        except (AssertionError, ValueError):
            violations.append((i, size_str))

    assert not violations, (
        "The following lines have a non-positive or non-integer size_kib "
        "value (3rd column):\n"
        + "\n".join(f"  line {ln}: {val!r}" for ln, val in violations)
    )


@pytest.mark.dependency(depends=["test_packages_file_tab_separated_and_three_columns"])
def test_no_header_or_comment_lines():
    """
    The spec says there is *no* header and no comment lines (e.g. lines
    starting with '#').  Ensure all lines start with a package name that
    begins with a letter or digit.
    """
    offending = []
    for i, line in enumerate(_read_packages_file(), start=1):
        first_char = line[0]
        if first_char == "#" or first_char.isspace():
            offending.append((i, line))

    assert not offending, (
        "packages.tsv must not contain header/comment lines. Offending "
        "lines:\n"
        + "\n".join(f"  line {ln}: {txt!r}" for ln, txt in offending)
    )