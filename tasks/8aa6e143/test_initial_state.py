# test_initial_state.py
#
# This test-suite validates that the *initial* filesystem state required for
# the “top 3 biggest CI build directories” assignment is present **before**
# the student runs their solution.
#
# It deliberately does NOT check for the output directory or file
# (/home/user/reports or /home/user/reports/top_dirs.log) because those are
# expected to be created by the student’s code.

import os
import stat
import pytest

# Base paths
CI_BUILDS_DIR = "/home/user/ci-builds"

# Expected first-level directories and the *exact* size in bytes of the single
# dummy.bin file that must exist in each of them.
#
# The files were created with:
#     dd if=/dev/zero of=dummy.bin bs=1M count=<N>
# so each “MB” is 1 048 576 bytes (1024 × 1024).
EXPECTED_LAYOUT = {
    "artifacts":   25 * 1_048_576,   # 25 MB
    "android-app": 12 * 1_048_576,   # 12 MB
    "cache":       10 * 1_048_576,   # 10 MB
    "ios-app":      8 * 1_048_576,   #  8 MB
    "shared-lib":   5 * 1_048_576,   #  5 MB
}


def _full_path(subdir: str) -> str:
    """Return the absolute path for a first-level directory inside ci-builds."""
    return os.path.join(CI_BUILDS_DIR, subdir)


@pytest.mark.describe("Initial filesystem layout for /home/user/ci-builds")
class TestInitialState:
    def test_ci_builds_directory_exists(self):
        assert os.path.exists(CI_BUILDS_DIR), (
            f"Required directory {CI_BUILDS_DIR!r} is missing."
        )
        assert stat.S_ISDIR(os.stat(CI_BUILDS_DIR).st_mode), (
            f"{CI_BUILDS_DIR!r} exists but is not a directory."
        )

    def test_expected_subdirectories_present(self):
        existing_subdirs = {
            name for name in os.listdir(CI_BUILDS_DIR)
            if os.path.isdir(_full_path(name))
        }

        # 1. All required subdirectories are present.
        missing = set(EXPECTED_LAYOUT) - existing_subdirs
        assert not missing, (
            "The following required subdirectories are missing under "
            f"{CI_BUILDS_DIR!r}: {', '.join(sorted(missing))}"
        )

        # 2. No unexpected extra subdirectories are present.
        extra = existing_subdirs - set(EXPECTED_LAYOUT)
        assert not extra, (
            "Unexpected subdirectories found under "
            f"{CI_BUILDS_DIR!r}: {', '.join(sorted(extra))}"
        )

    @pytest.mark.parametrize("subdir,expected_size", EXPECTED_LAYOUT.items())
    def test_dummy_bin_exists_with_correct_size(self, subdir, expected_size):
        dummy_path = os.path.join(_full_path(subdir), "dummy.bin")

        assert os.path.exists(dummy_path), (
            f"File {dummy_path!r} is missing."
        )
        assert stat.S_ISREG(os.stat(dummy_path).st_mode), (
            f"{dummy_path!r} exists but is not a regular file."
        )

        actual_size = os.path.getsize(dummy_path)
        assert actual_size == expected_size, (
            f"Size mismatch for {dummy_path!r}: expected {expected_size} bytes, "
            f"found {actual_size} bytes."
        )