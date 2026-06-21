# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem BEFORE the
# student runs any commands.  The tests assert that the three original build
# log files exist with the expected pre-task characteristics, and that the
# output artefacts requested in the task description do NOT yet exist.
#
# Only Python stdlib and pytest are used.

import os
from pathlib import Path
import stat
import pytest

# ---------------------------------------------------------------------------
# Constants – absolute paths that must already exist on the VM
# ---------------------------------------------------------------------------

HOME = Path("/home/user").resolve()
BUILDS_DIR = HOME / "builds"

LOG_PATHS = [
    BUILDS_DIR / "2023-05-01" / "artifacts.log",
    BUILDS_DIR / "2023-05-02" / "artifacts.log",
    BUILDS_DIR / "2023-05-03" / "artifacts.log",
]

# Files that MUST NOT exist before the student starts
OUTPUT_CSV = BUILDS_DIR / "all_artifacts_clean.csv"
SUMMARY_TXT = BUILDS_DIR / "artifact_summary.txt"

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------


def readable_by_world(path: Path) -> bool:
    """Return True if 'path' is readable by 'other' (world) users."""
    mode = path.stat().st_mode
    return bool(mode & stat.S_IROTH)


def iter_build_files(root: Path):
    """Yield all regular files under *root* (recursive)."""
    for dirpath, _dirnames, filenames in os.walk(root):
        for fn in filenames:
            yield Path(dirpath, fn)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_builds_directory_exists():
    assert BUILDS_DIR.is_dir(), (
        f"Expected directory {BUILDS_DIR} to exist before the task begins."
    )


@pytest.mark.parametrize("log_path", LOG_PATHS)
def test_log_files_exist_and_are_world_readable(log_path: Path):
    assert log_path.is_file(), f"Missing expected log file: {log_path}"
    assert readable_by_world(
        log_path
    ), f"Log file {log_path} should be world-readable (mode 0o644 or similar)."


def test_each_log_line_has_five_pipe_delimited_fields():
    for log_path in LOG_PATHS:
        with log_path.open("r", encoding="utf-8") as fh:
            lines = [ln.rstrip("\n") for ln in fh]
        assert lines, f"{log_path} is unexpectedly empty."

        for lineno, line in enumerate(lines, 1):
            parts = line.split("|")
            assert len(parts) == 5, (
                f"{log_path}:{lineno} – expected exactly 5 '|'-delimited fields "
                f"but found {len(parts)}. Line content: {line!r}"
            )
            status = parts[-1]
            assert status in {
                "OK",
                "FAIL",
            }, f"{log_path}:{lineno} – status must be 'OK' or 'FAIL', got {status!r}"


def test_fail_tokens_present_before_student_starts():
    fail_count = 0
    for log_path in LOG_PATHS:
        text = log_path.read_text(encoding="utf-8")
        fail_count += text.count("|FAIL")
    assert (
        fail_count > 0
    ), "There should be at least one '|FAIL' token in the raw logs before the task begins."


def test_no_retry_pending_tokens_yet():
    retry_count = 0
    # check every file under /home/user/builds just in case
    for file_path in iter_build_files(BUILDS_DIR):
        if file_path.is_file():
            retry_count += file_path.read_text(encoding="utf-8").count("RETRY_PENDING")
    assert (
        retry_count == 0
    ), "Found 'RETRY_PENDING' tokens before the task started; logs must not be pre-patched."


def test_output_files_do_not_exist_yet():
    assert not OUTPUT_CSV.exists(), (
        f"{OUTPUT_CSV} should NOT exist before the student runs their solution."
    )
    assert not SUMMARY_TXT.exists(), (
        f"{SUMMARY_TXT} should NOT exist before the student runs their solution."
    )