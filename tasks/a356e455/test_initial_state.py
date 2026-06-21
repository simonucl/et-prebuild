# test_initial_state.py
"""
Pytest suite to validate the pre-existing filesystem state **before** the student
performs any actions for the “translation log summary” exercise.

What we check:
1. The log file /home/user/projects/app/locale/translation_update.log exists,
   is a regular file and is readable.
2. The file contains exactly the five expected lines (no leading spaces on
   any line) and terminates with a single LF newline.
3. We deliberately do *not* check for the reports directory or the summary file
   because those are artefacts that should be created by the student.
"""

import io
from pathlib import Path
import pytest

LOG_PATH = Path("/home/user/projects/app/locale/translation_update.log")

EXPECTED_LINES = [
    "[INFO] 2023-11-10 10:00:00 Added translation key: welcome_message",
    "[WARNING] 2023-11-10 10:01:00 Missing translation for key: goodbye_message",
    "[INFO] 2023-11-10 10:02:00 Updated translation key: help_message",
    "[ERROR] 2023-11-10 10:03:00 Duplicate translation key: welcome_message",
    "[INFO] 2023-11-10 10:04:00 Added translation key: new_feature_message",
]


def test_log_file_exists_and_is_readable():
    """
    Ensure the translation update log exists, is a file (not a directory or
    symlink), and is readable.
    """
    assert LOG_PATH.exists(), f"Required log file not found at {LOG_PATH}"
    assert LOG_PATH.is_file(), f"Expected a regular file at {LOG_PATH}, " \
                               f"but found something else"
    try:
        LOG_PATH.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Log file exists but could not be read: {exc}")


def test_log_file_contents_exact_match():
    """
    Validate that the log file content is exactly the five expected lines,
    each ending with a Unix LF newline, and with no extra blank lines
    or leading spaces.
    """
    raw_content = LOG_PATH.read_bytes()

    # 1. File must terminate with a single LF.
    assert raw_content.endswith(b"\n"), (
        "Log file must end with a single Unix newline (LF)"
    )

    # 2. Split into lines (strip the trailing LF to avoid an empty last element).
    # Using io.BytesIO to avoid decoding issues and to preserve exact data.
    lines = io.BytesIO(raw_content).read().rstrip(b"\n").decode("utf-8").split("\n")

    # 3. Verify number of lines.
    assert len(lines) == 5, (
        f"Log file should contain exactly 5 lines, found {len(lines)}"
    )

    # 4. Verify exact line content.
    for idx, (expected, found) in enumerate(zip(EXPECTED_LINES, lines), start=1):
        assert found == expected, (
            f"Line {idx} mismatch:\n"
            f"  Expected: {expected!r}\n"
            f"  Found:    {found!r}"
        )