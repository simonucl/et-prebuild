# test_initial_state.py
"""
Pytest suite that validates the expected *initial* filesystem state before the
student executes any update-automation.  Only the original Kubernetes manifest
tree is inspected; no checks are performed against the yet-to-be-created
/output/ artefacts.

The tests assert:

1. The /home/user/manifests directory exists.
2. All six expected manifest files are present at the exact absolute paths.
3. Exactly three specific files still contain the un-pinned line
      image: nginx
   (and do *not* yet contain a version tag).
4. No other file accidentally contains that un-pinned image line.
"""

import os
import re
from pathlib import Path

import pytest

BASE_DIR = Path("/home/user/manifests").resolve()

# --------------------------------------------------------------------------- #
# 1. Directory existence
# --------------------------------------------------------------------------- #
def test_manifests_directory_exists():
    assert BASE_DIR.is_dir(), f"Required directory {BASE_DIR} is missing."


# --------------------------------------------------------------------------- #
# 2. File presence
# --------------------------------------------------------------------------- #
ALL_EXPECTED_FILES = [
    "dep_proxy.yaml",
    "ns1/dep-nginx.yaml",
    "ns1/svc.yaml",
    "ns2/dep-api.yaml",
    "ns2/dep-nginx-2.yml",
    "ns3/job.yaml",
]


@pytest.mark.parametrize("relative_path", ALL_EXPECTED_FILES)
def test_expected_files_exist(relative_path):
    abs_path = BASE_DIR / relative_path
    assert abs_path.is_file(), f"Expected manifest file {abs_path} is missing."


# --------------------------------------------------------------------------- #
# 3. Content validation
# --------------------------------------------------------------------------- #

# Files that *should* start out with the untagged nginx reference
FILES_WITH_UNTAGGED_NGINX = [
    "dep_proxy.yaml",
    "ns1/dep-nginx.yaml",
    "ns2/dep-nginx-2.yml",
]

# Compiled regex for an exact line: optional leading spaces, 'image:', single
# space, 'nginx', nothing else on the line.
UNTAGGED_PATTERN = re.compile(r"^\s*image:\s+nginx\s*$", re.MULTILINE)

# Same idea but for an already-tagged nginx image (which must NOT be present yet)
TAGGED_PATTERN = re.compile(r"^\s*image:\s+nginx:.*$", re.MULTILINE)


@pytest.mark.parametrize("relative_path", FILES_WITH_UNTAGGED_NGINX)
def test_files_still_contain_untagged_nginx(relative_path):
    abs_path = BASE_DIR / relative_path
    content = abs_path.read_text()
    assert UNTAGGED_PATTERN.search(
        content
    ), (
        f"File {abs_path} should still contain an untagged "
        f"'image: nginx' line before the upgrade."
    )
    assert not TAGGED_PATTERN.search(
        content
    ), f"File {abs_path} already appears to have a version tag; expected initial state."


# Files that must *not* have an untagged nginx line to begin with
FILES_WITHOUT_UNTAGGED_NGINX = sorted(
    set(ALL_EXPECTED_FILES) - set(FILES_WITH_UNTAGGED_NGINX)
)


@pytest.mark.parametrize("relative_path", FILES_WITHOUT_UNTAGGED_NGINX)
def test_other_files_do_not_contain_untagged_nginx(relative_path):
    abs_path = BASE_DIR / relative_path
    content = abs_path.read_text()
    assert not UNTAGGED_PATTERN.search(
        content
    ), f"File {abs_path} unexpectedly contains an untagged 'image: nginx' line."