# test_initial_state.py
#
# Pytest suite that validates the initial OS / filesystem state
# before the student begins work on the PCI-DSS audit task.

import os
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants describing the expected initial filesystem layout
# ---------------------------------------------------------------------------

HOME = Path("/home/user")

COMPLIANCE_ROOT = HOME / "compliance"

PCI_MATCHING_FILES = [
    # path relative to /home/user
    ("compliance/2021/archive/old_payment.md", 1),
    ("compliance/2021/payments_policy.txt", 2),
    ("compliance/2022/network_controls.md", 2),
    ("compliance/2023/draft/pci_overview.md", 3),
]

NON_MATCHING_FILES = [
    "compliance/2022/README.txt",  # 0 occurrences of “PCI-DSS”
]


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------


def _assert_regular_file(path: Path):
    """
    Assert that `path` exists and is a regular file (not a directory or symlink).
    """
    assert path.exists(), f"Expected file to exist: {path}"
    assert path.is_file(), f"Expected a regular file (not a directory): {path}"
    # `Path.is_file()` follows symlinks, so we additionally disallow symlinks.
    assert not path.is_symlink(), f"File must not be a symlink: {path}"


def _count_token(path: Path, token: str = "PCI-DSS") -> int:
    """
    Return the number of exact, case-sensitive occurrences of `token`
    in the text file located at `path`.
    """
    with path.open("r", encoding="utf-8") as fh:
        data = fh.read()
    return data.count(token)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_compliance_root_exists_and_is_directory():
    assert COMPLIANCE_ROOT.exists(), f"Missing directory: {COMPLIANCE_ROOT}"
    assert COMPLIANCE_ROOT.is_dir(), f"Path is not a directory: {COMPLIANCE_ROOT}"
    assert not COMPLIANCE_ROOT.is_symlink(), f"Directory must not be a symlink: {COMPLIANCE_ROOT}"


@pytest.mark.parametrize("rel_path,expected_mentions", PCI_MATCHING_FILES)
def test_pci_matching_files_exist_and_have_correct_counts(rel_path, expected_mentions):
    """
    For every file that is supposed to contain the token 'PCI-DSS',
    verify that:
      1) The file exists as a regular file.
      2) The exact number of token occurrences matches the ground truth.
    """
    absolute_path = HOME / rel_path
    _assert_regular_file(absolute_path)

    occurrences = _count_token(absolute_path, token="PCI-DSS")
    assert (
        occurrences == expected_mentions
    ), f"{absolute_path}: expected {expected_mentions} occurrences of 'PCI-DSS', found {occurrences}"


@pytest.mark.parametrize("rel_path", NON_MATCHING_FILES)
def test_non_matching_files_have_zero_mentions(rel_path):
    """
    Files that are known *not* to contain 'PCI-DSS' must indeed have zero occurrences.
    """
    absolute_path = HOME / rel_path
    _assert_regular_file(absolute_path)

    occurrences = _count_token(absolute_path, token="PCI-DSS")
    assert (
        occurrences == 0
    ), f"{absolute_path}: expected 0 occurrences of 'PCI-DSS', found {occurrences}"


def test_only_listed_files_contain_pci_dss_token():
    """
    Sanity check across the entire compliance tree:

    Ensure that no *unexpected* .txt or .md files already contain the
    'PCI-DSS' token.  This guarantees that the answer key is complete
    before the student begins working.

    (If future tasks add additional matching files, this test will alert
    the curriculum maintainers.)
    """
    expected_paths = {str(HOME / p[0]) for p in PCI_MATCHING_FILES}

    for root, dirs, files in os.walk(COMPLIANCE_ROOT):
        # Skip symlinks to remain consistent with the task spec
        dirs[:] = [d for d in dirs if not Path(root, d).is_symlink()]

        for fname in files:
            if not fname.endswith((".txt", ".md")):
                continue

            fpath = Path(root) / fname
            # Ignore symlinks to files
            if fpath.is_symlink():
                continue

            if "PCI-DSS" in fpath.read_text(encoding="utf-8"):
                assert (
                    str(fpath) in expected_paths
                ), (
                    f"Unexpected file contains 'PCI-DSS': {fpath}\n"
                    "If this file is part of the intended fixture, add it to "
                    "PCI_MATCHING_FILES with the correct mention count."
                )


# ---------------------------------------------------------------------------
# End of file
# ---------------------------------------------------------------------------