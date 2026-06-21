# test_initial_state.py
#
# This pytest suite validates the **initial** operating-system / filesystem
# state before the student performs any actions.

import pathlib
import pytest

PROFILING_DIR = pathlib.Path("/home/user/profiling")
EXPECTED_PERF_FILES = {
    "cpu_usage.perf",
    "mem_usage.perf",
    "io_usage.perf",
}


def test_profiling_directory_exists():
    """
    The directory that stores raw profiling data **must** exist before any
    backup commands are executed.
    """
    assert PROFILING_DIR.exists(), (
        "Required directory '/home/user/profiling' does not exist.  "
        "Create it (and the expected .perf files) before proceeding."
    )
    assert PROFILING_DIR.is_dir(), (
        f"'{PROFILING_DIR}' exists but is not a directory.  "
        "Ensure it is a regular directory that will hold .perf files."
    )


def test_required_perf_files_present_and_no_extras():
    """
    1. All three expected '.perf' files must already be present.
    2. No additional '.perf' files should exist at this point—keeping the
       starting conditions predictable for the backup script.
    """
    found_perf_files = {
        path.name
        for path in PROFILING_DIR.iterdir()
        if path.is_file() and path.suffix == ".perf"
    }

    missing = EXPECTED_PERF_FILES - found_perf_files
    extra = found_perf_files - EXPECTED_PERF_FILES

    assert not missing, (
        "The following required '.perf' files are missing in "
        f"'{PROFILING_DIR}': {sorted(missing)}"
    )
    assert not extra, (
        "Unexpected '.perf' files found in "
        f"'{PROFILING_DIR}': {sorted(extra)}\n"
        "Remove or relocate these files so the backup contains exactly the "
        "intended three files."
    )


@pytest.mark.parametrize("filename", sorted(EXPECTED_PERF_FILES))
def test_perf_files_are_non_empty_and_readable(filename):
    """
    Sanity-check that each expected '.perf' file is readable and contains
    at least one non-whitespace character.  Empty or unreadable files would
    indicate a problem with the test fixture setup.
    """
    file_path = PROFILING_DIR / filename
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(
            f"Failed to read '{file_path}': {exc}\n"
            "Ensure the file exists and has appropriate read permissions."
        )

    assert content.strip(), f"File '{file_path}' is empty; it should contain profiling data."