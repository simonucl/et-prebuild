# test_initial_state.py
#
# Pytest suite that validates the *initial* on-disk layout
# before the student starts the clean-up task.
#
# Rules checked:
#   • /home/user/container_repo exists and is a directory.
#   • Exactly the five expected “.sif” files are present there.
#   • Each file has the exact byte size dictated by the spec.
#   • No extra “.sif” files are present.
#
# NOTE:  We intentionally do **not** test for the existence or absence of any
#        output artefacts (e.g., /home/user/old_containers or cleanup.log)
#        because those belong to the post-task state.

import os
from pathlib import Path

import pytest

CONTAINER_REPO = Path("/home/user/container_repo")

# Expected .sif files and their exact byte sizes
EXPECTED_SIFS = {
    "alpine_3.12.sif": 5_242_880,   # 5  MiB
    "centos_7.sif":    7_340_032,   # 7  MiB
    "debian_10.sif":  11_288_576,   # ~10.8 MiB
    "ubuntu_18.04.sif": 12_582_912, # 12 MiB
    "ubuntu_20.04.sif": 15_728_640, # 15 MiB
}

@pytest.fixture(scope="module")
def repo_contents():
    """Return a mapping of file name -> Path for *.sif files in the repo."""
    if not CONTAINER_REPO.exists():
        pytest.fail(f"Required directory {CONTAINER_REPO} is missing.")
    if not CONTAINER_REPO.is_dir():
        pytest.fail(f"{CONTAINER_REPO} exists but is not a directory.")
    sif_paths = {p.name: p for p in CONTAINER_REPO.glob("*.sif")}
    return sif_paths

def test_exactly_expected_files_present(repo_contents):
    """Verify that *only* the five expected .sif files exist in the repo."""
    present = set(repo_contents.keys())
    expected = set(EXPECTED_SIFS.keys())

    missing = expected - present
    extra   = present - expected

    if missing:
        pytest.fail(f"Missing expected .sif file(s): {', '.join(sorted(missing))}")
    if extra:
        pytest.fail(f"Found unexpected .sif file(s): {', '.join(sorted(extra))}")

def test_file_sizes_are_correct(repo_contents):
    """Verify each .sif file has the exact byte size specified."""
    for name, expected_size in EXPECTED_SIFS.items():
        path = repo_contents[name]
        actual_size = path.stat().st_size
        assert actual_size == expected_size, (
            f"Size mismatch for {path} — expected {expected_size} bytes, "
            f"found {actual_size} bytes."
        )