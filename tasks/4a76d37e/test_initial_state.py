# test_initial_state.py
#
# This pytest suite verifies the *initial* state of the file-system
# before the student starts working on the task.  It checks that
# 1. The source log file is present with the exact expected content.
# 2. No output directory or files from the end-state requirements
#    have been created yet.
#
# Only the Python standard library and pytest are used.

from pathlib import Path
import os
import stat
import pytest

HOME = Path("/home/user")
SOURCE_LOG = HOME / "repository_uploads.log"
CURATED_DIR = HOME / "curated"
ERROR_LOG = CURATED_DIR / "upload_errors_2023-09.log"
SUMMARY_FILE = CURATED_DIR / "error_summary.txt"

EXPECTED_LINES = [
    "2023-08-30 12:45:01 INFO repoA artifact aaa-1.0.jar uploaded successfully\n",
    "2023-08-30 12:46:17 ERROR repoB artifact bbb-2.1.jar checksum mismatch\n",
    "2023-08-31 09:15:33 WARN repoC artifact ccc-3.0.jar deprecated classifier\n",
    "2023-09-01 08:00:14 INFO repoA artifact aaa-1.1.jar uploaded successfully\n",
    "2023-09-01 08:02:55 ERROR repoA artifact aaa-1.1.jar checksum mismatch\n",
    "2023-09-02 10:20:43 ERROR repoC artifact ccc-3.1.jar signature invalid\n",
    "2023-09-02 11:00:00 INFO repoB artifact bbb-2.2.jar uploaded successfully\n",
    "2023-09-03 07:30:22 INFO repoD artifact ddd-4.0.jar uploaded successfully\n",
    "2023-09-03 07:32:10 ERROR repoD artifact ddd-4.0.jar checksum mismatch\n",
    "2023-09-04 09:00:00 WARN repoA artifact aaa-1.2.jar large file size\n",
    "2023-09-04 09:01:30 ERROR repoB artifact bbb-2.2.jar signature invalid\n",
    "2023-09-05 13:22:17 INFO repoC artifact ccc-3.1.jar uploaded successfully\n",
    "2023-09-05 13:23:02 ERROR repoC artifact ccc-3.1.jar timeout during replication\n",
    "2023-09-05 13:25:47 INFO repoA artifact aaa-1.2.jar uploaded successfully\n",
    "2023-09-06 15:40:00 ERROR repoE artifact eee-5.0.jar checksum mismatch\n",
]


def test_source_log_exists_and_is_regular_file():
    assert SOURCE_LOG.exists(), f"Expected source log file {SOURCE_LOG} to exist."
    assert SOURCE_LOG.is_file(), f"{SOURCE_LOG} exists but is not a regular file."


def test_source_log_content_exact_match():
    # Read the entire file as UTF-8; this will raise UnicodeDecodeError
    # if the encoding is wrong, causing the test to fail.
    data = SOURCE_LOG.read_text(encoding="utf-8")
    # Ensure file ends with a single trailing newline.
    assert data.endswith(
        "\n"
    ), f"{SOURCE_LOG} must end with a single trailing newline (LF)."

    lines = data.splitlines(keepends=True)
    assert (
        len(lines) == 15
    ), f"{SOURCE_LOG} should contain exactly 15 lines, found {len(lines)}."

    # Compare line-by-line so the assertion error shows the first mismatch
    for idx, (expected, actual) in enumerate(zip(EXPECTED_LINES, lines), start=1):
        assert (
            expected == actual
        ), f"Line {idx} mismatch in {SOURCE_LOG!s}.\nExpected: {expected!r}\nActual:   {actual!r}"


@pytest.mark.parametrize(
    "path_description, path_object",
    [
        ("curated directory", CURATED_DIR),
        ("filtered error log", ERROR_LOG),
        ("summary file", SUMMARY_FILE),
    ],
)
def test_no_output_artifacts_exist_yet(path_description, path_object: Path):
    assert not path_object.exists(), (
        f"Pre-condition failed: {path_description} ({path_object}) should NOT exist "
        "before the student performs any actions."
    )