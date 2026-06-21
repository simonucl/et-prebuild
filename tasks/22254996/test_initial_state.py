# test_initial_state.py
#
# Pytest suite that verifies the **initial** repository layout before the
# student performs any clean-up actions.  It checks only the pre-existing
# files and directories that must already be present.  It does *not* look for
# the “deprecated” directory or the log file, because those are part of the
# work the student still has to do.

import os
import stat
import pytest

HOME = "/home/user"
ARTIFACTS_DIR = os.path.join(HOME, "artifacts")
STABLE_DIR = os.path.join(ARTIFACTS_DIR, "stable")
TESTING_DIR = os.path.join(ARTIFACTS_DIR, "testing")

# Mapping of absolute file paths to the exact ASCII content they must contain.
EXPECTED_FILES = {
    os.path.join(STABLE_DIR, "library-1.0.jar"): "release build 1.0\n",
    os.path.join(STABLE_DIR, "library-1.1-SNAPSHOT.jar"): "snapshot build 1.1\n",
    os.path.join(TESTING_DIR, "tool-2.0.jar"): "release build 2.0\n",
    os.path.join(TESTING_DIR, "tool-2.0-SNAPSHOT.jar"): "snapshot build 2.0\n",
}


def _assert_mode(path: str, expected: int, what: str) -> None:
    """Helper: ensure a given permission bit is set on *path*."""
    mode = os.stat(path).st_mode
    assert mode & expected, f"{what} '{path}' should have permission bit {oct(expected)} set"


def test_artifacts_directory_structure():
    """Top-level directory layout must already exist."""
    assert os.path.isdir(ARTIFACTS_DIR), f"Missing directory: {ARTIFACTS_DIR}"
    assert os.path.isdir(STABLE_DIR), f"Missing directory: {STABLE_DIR}"
    assert os.path.isdir(TESTING_DIR), f"Missing directory: {TESTING_DIR}"

    # The artifacts directory should at least contain “stable” and “testing”.
    entries = set(os.listdir(ARTIFACTS_DIR))
    for d in ("stable", "testing"):
        assert d in entries, f"Directory {d} is missing inside {ARTIFACTS_DIR}"


@pytest.mark.parametrize("path,expected_content", EXPECTED_FILES.items())
def test_initial_files_present_with_correct_content(path, expected_content):
    """Each expected JAR file must exist and contain the exact ASCII payload."""
    assert os.path.isfile(path), f"Required file missing: {path}"

    # Ensure it has owner read (stat.S_IRUSR) permission so the student can work with it.
    _assert_mode(path, stat.S_IRUSR, "File")

    # Read the file as text; the fixtures are ASCII strings.
    with open(path, "r", encoding="utf-8") as fh:
        content = fh.read()
    assert (
        content == expected_content
    ), f"File {path} contains unexpected data.\nExpected: {expected_content!r}\nFound:    {content!r}"


def test_no_extra_files_inside_stable_and_testing():
    """Only the four predefined JARs must be inside their respective folders."""
    stable_expected = {"library-1.0.jar", "library-1.1-SNAPSHOT.jar"}
    testing_expected = {"tool-2.0.jar", "tool-2.0-SNAPSHOT.jar"}

    stable_actual = set(os.listdir(STABLE_DIR))
    testing_actual = set(os.listdir(TESTING_DIR))

    assert stable_actual == stable_expected, (
        "Unexpected contents in 'stable' directory.\n"
        f"Expected: {sorted(stable_expected)}\n"
        f"Found:    {sorted(stable_actual)}"
    )
    assert testing_actual == testing_expected, (
        "Unexpected contents in 'testing' directory.\n"
        f"Expected: {sorted(testing_expected)}\n"
        f"Found:    {sorted(testing_actual)}"
    )