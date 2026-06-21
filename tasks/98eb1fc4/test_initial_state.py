# test_initial_state.py
#
# This test-suite validates that the workspace is still in its original
# (pre-exercise) state.  In other words, the artefacts that the student is
# supposed to create MUST NOT exist yet.

from pathlib import Path
import pytest

# Absolute paths that will be created by the student _later_.
OBS_LOG_DIR = Path("/home/user/observability/logs")
TUNING_FILE = OBS_LOG_DIR / "tuning_status.json"

# The exact JSON document expected _after_ the student finishes the task.
EXPECTED_JSON = (
    '{\n'
    '  "dashboard": "latency-overview",\n'
    '  "tuned": true,\n'
    '  "timestamp": "2023-09-10T00:00:00Z"\n'
    '}\n'
)


def test_logs_directory_absent_or_empty():
    """
    The directory '/home/user/observability/logs' should NOT exist yet.
    If '/home/user/observability' (the parent) already exists for some
    unrelated reason, that is fine, but the 'logs' directory itself must
    be absent until the student creates it.
    """
    assert not OBS_LOG_DIR.exists(), (
        f"The directory {OBS_LOG_DIR} already exists, but it should be "
        "created by the student as part of the exercise."
    )


def test_tuning_status_file_absent():
    """
    The file 'tuning_status.json' must not be present before the student
    runs their command.  Its presence would indicate the workspace is not
    in a clean initial state.
    """
    assert not TUNING_FILE.exists(), (
        f"The file {TUNING_FILE} already exists. "
        "The workspace must start without this file."
    )


def test_no_preexisting_matching_content(tmp_path):
    """
    Guard against a scenario where a file with the target path exists
    but contains *some other* data.  If such a file is found, fail with a
    clear message so the student starts from a known-good baseline.
    """
    if TUNING_FILE.exists():
        content = TUNING_FILE.read_text(encoding="utf-8", errors="replace")
        assert content != EXPECTED_JSON, (
            f"The file {TUNING_FILE} already contains the expected final "
            "JSON.  The exercise should begin without this content."
        )