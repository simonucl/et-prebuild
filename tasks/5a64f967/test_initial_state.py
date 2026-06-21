# test_initial_state.py
#
# Pytest suite that validates the **initial** on-disk state of the workspace
# before the student’s solution is executed.
#
# It checks that:
#   • The expected directory tree exists.
#   • Exactly three regular files are present.
#   • The byte-sizes of each file match the problem statement.
#   • No unexpected files are lurking in the workspace.
#
# Only the Python standard library and pytest are used.

from pathlib import Path
import os
import pytest

WORKSPACE_ROOT = Path("/home/user/workspace").resolve()

# Expected files (absolute paths) → expected size in bytes
EXPECTED_FILES = {
    WORKSPACE_ROOT / "file1.txt": 1024,
    WORKSPACE_ROOT / "file2.log": 2048,
    WORKSPACE_ROOT / "logs" / "archive" / "file3.gz": 4096,
}

EXPECTED_TOTAL_SIZE = sum(EXPECTED_FILES.values())


@pytest.fixture(scope="session")
def discovered_files():
    """
    Return a dict mapping Path → size for every *regular* file discovered
    under the workspace root.
    """
    if not WORKSPACE_ROOT.exists():
        pytest.fail(f"Workspace directory {WORKSPACE_ROOT} is missing.")

    files = {}
    for path in WORKSPACE_ROOT.rglob("*"):
        # We only care about regular files; skip dirs, symlinks, etc.
        if path.is_file():
            try:
                size = path.stat().st_size
            except OSError as exc:
                pytest.fail(f"Could not stat {path}: {exc}")
            files[path] = size
    return files


def test_expected_directories_exist():
    """Validate that the expected directory hierarchy is present."""
    dir_paths = [
        WORKSPACE_ROOT,
        WORKSPACE_ROOT / "logs",
        WORKSPACE_ROOT / "logs" / "archive",
    ]
    for dpath in dir_paths:
        assert dpath.is_dir(), f"Required directory {dpath} is missing."


def test_all_expected_files_present(discovered_files):
    """Every expected file must exist and have the correct size."""
    for path, expected_size in EXPECTED_FILES.items():
        assert path in discovered_files, f"Expected file {path} is missing."
        actual_size = discovered_files[path]
        assert (
            actual_size == expected_size
        ), f"File {path} has size {actual_size}B, expected {expected_size}B."


def test_no_unexpected_files(discovered_files):
    """No extra regular files should be present in the workspace tree."""
    unexpected = sorted(set(discovered_files) - set(EXPECTED_FILES))
    assert (
        not unexpected
    ), f"Unexpected file(s) found under {WORKSPACE_ROOT}: {', '.join(map(str, unexpected))}"


def test_total_size_matches(discovered_files):
    """The sum of all file sizes must match the stated total."""
    total_size = sum(discovered_files.values())
    assert (
        total_size == EXPECTED_TOTAL_SIZE
    ), f"Total size {total_size}B does not match expected {EXPECTED_TOTAL_SIZE}B."