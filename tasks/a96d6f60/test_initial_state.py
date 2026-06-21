# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the filesystem
# before the student performs any action for the “release-summary.log”
# exercise.  It checks that:
#
#   • The expected directory hierarchy exists.
#   • The exact set of JAR artifacts is present (no more, no fewer).
#   • Each JAR has the expected byte-size.
#   • The output file (/home/user/builds/release-summary.log) does NOT
#     exist yet.
#
# Only stdlib + pytest are used.

import os
import stat
import pytest

HOME = "/home/user"
BUILDS_DIR = os.path.join(HOME, "builds")
ARTIFACTS_DIR = os.path.join(BUILDS_DIR, "artifacts")
RELEASE_SUMMARY = os.path.join(BUILDS_DIR, "release-summary.log")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def file_size(path):
    """Return the size of *path* in raw bytes."""
    return os.stat(path)[stat.ST_SIZE]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_build_directories_exist():
    """Validate that /home/user/builds and its artifacts subdirectory exist."""
    assert os.path.isdir(
        BUILDS_DIR
    ), f"Expected directory {BUILDS_DIR!r} to exist, but it is missing or not a directory."

    assert os.path.isdir(
        ARTIFACTS_DIR
    ), f"Expected directory {ARTIFACTS_DIR!r} to exist, but it is missing or not a directory."


def test_expected_artifacts_are_present_and_only_them():
    """
    Exactly three JAR files must be present in the artifacts directory,
    and their filenames must match the specification.
    """
    expected = {
        "app-core-1.2.0.jar",
        "app-core-1.2.1-SNAPSHOT.jar",
        "app-ui-1.2.0.jar",
    }

    actual = {f for f in os.listdir(ARTIFACTS_DIR) if f.endswith(".jar")}

    missing = expected - actual
    extra = actual - expected

    assert not missing, (
        "The following expected JAR(s) are missing from "
        f"{ARTIFACTS_DIR!r}: {', '.join(sorted(missing))}"
    )
    assert not extra, (
        "Unexpected JAR file(s) found in "
        f"{ARTIFACTS_DIR!r}: {', '.join(sorted(extra))}. "
        "The directory must contain only the specified artifacts."
    )


@pytest.mark.parametrize(
    "filename,expected_size",
    [
        ("app-core-1.2.0.jar", 19),
        ("app-ui-1.2.0.jar", 17),
        ("app-core-1.2.1-SNAPSHOT.jar", 28),
    ],
)
def test_artifact_sizes_are_correct(filename, expected_size):
    """Each JAR file must have the exact byte-size expected."""
    path = os.path.join(ARTIFACTS_DIR, filename)
    assert os.path.isfile(
        path
    ), f"Expected file {path!r} to exist, but it is missing."

    actual_size = file_size(path)
    assert (
        actual_size == expected_size
    ), f"Size mismatch for {filename!r}: expected {expected_size} bytes, got {actual_size} bytes."


def test_release_summary_log_does_not_exist_yet():
    """
    The summary file should NOT exist before the student runs their solution.
    Its presence would indicate that the environment is not clean.
    """
    assert not os.path.exists(
        RELEASE_SUMMARY
    ), f"File {RELEASE_SUMMARY!r} should not exist before the task is attempted."