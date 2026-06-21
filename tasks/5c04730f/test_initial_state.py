# test_initial_state.py
#
# This test-suite verifies that the raw CI log files which the student is
# supposed to parse are present *before* any student code is executed and that
# the critical information we expect to be in those logs is actually there.
#
# IMPORTANT:  We intentionally do **not** check for the presence (or absence)
# of any output artefacts such as “/home/user/build_reports/” or
# “build_summary.tsv”, because those belong to the *solution* stage and must
# not be part of the initial-state validation.
#
# The tests rely on Python’s standard library only and should run on any
# POSIX-compatible system.

import pathlib
import pytest

LOG_DIR = pathlib.Path("/home/user/build_logs")

ANDROID_LOG = LOG_DIR / "build_android.log"
IOS_LOG = LOG_DIR / "build_ios.log"


@pytest.mark.parametrize(
    "file_path",
    [ANDROID_LOG, IOS_LOG],
    ids=["android_log_exists", "ios_log_exists"],
)
def test_log_files_exist(file_path):
    """
    Make sure each required log file exists and is a regular file.
    """
    assert file_path.exists(), f"Expected log file {file_path} is missing."
    assert file_path.is_file(), f"{file_path} exists but is not a regular file."


def _assert_lines_present(text: str, expected_lines: list[str], file_path: pathlib.Path):
    """
    Helper that verifies every line in `expected_lines` occurs somewhere
    in the file content `text`.  Raises an informative assertion on failure.
    """
    missing = [line for line in expected_lines if line not in text]
    assert not missing, (
        f"{file_path} is present, but the following expected line(s) are missing or "
        f"spelled differently:\n    " + "\n    ".join(missing)
    )


def test_android_log_content():
    """
    Validate that build_android.log contains all the critical information
    the downstream task depends on (status, test counts, duration, etc.).
    """
    content = ANDROID_LOG.read_text(encoding="utf-8")

    expected_lines = [
        "[INFO] Build status: SUCCESS",
        "[INFO] Total tests run: 120",
        "[INFO] Tests failed: 3",
        "[INFO] Total time: 7 minutes 35 seconds",
    ]

    _assert_lines_present(content, expected_lines, ANDROID_LOG)


def test_ios_log_content():
    """
    Validate that build_ios.log contains all the critical information
    the downstream task depends on (status, test counts, duration, etc.).
    """
    content = IOS_LOG.read_text(encoding="utf-8")

    expected_lines = [
        "[INFO] Build status: FAILURE",
        "[INFO] Total tests run: 110",
        "[INFO] Tests failed: 11",
        "[INFO] Total time: 8 minutes 22 seconds",
    ]

    _assert_lines_present(content, expected_lines, IOS_LOG)


def test_log_directory_exists_and_only_expected_files_present():
    """
    The build_logs directory must exist and contain *at least* the two expected
    files.  This test also guards against the accidental presence of files that
    should not be there, signalling a contaminated initial state.
    """
    assert LOG_DIR.exists(), f"Directory {LOG_DIR} is missing."
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."

    # Collect the names of all regular files inside build_logs
    present_files = {p.name for p in LOG_DIR.iterdir() if p.is_file()}
    expected_files = {ANDROID_LOG.name, IOS_LOG.name}

    # Every expected file must be present
    missing = expected_files - present_files
    assert not missing, (
        f"The following expected file(s) are missing in {LOG_DIR}: {', '.join(sorted(missing))}"
    )

    # Fail if there are *unexpected* files which could interfere with testing
    unexpected = present_files - expected_files
    assert not unexpected, (
        f"The directory {LOG_DIR} contains unexpected file(s) that should not be part "
        f"of the pristine initial state: {', '.join(sorted(unexpected))}"
    )