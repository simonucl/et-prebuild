# test_initial_state.py
#
# This test-suite validates the **initial** state of the filesystem that
# students see *before* they run their solution.  If any of these tests
# fail, the exercise itself is mis-configured, not the student’s work.
#
# Rules enforced here:
#   1. /home/user/logs/combined.log must exist with the exact expected
#      contents (15 JSON records, newline-terminated).
#   2. The two artefacts that the student is supposed to create
#      (/home/user/incident_triage/filtered_2023-10-12_1400-1415.log and
#      /home/user/incident_triage/error_summary.txt) must **not** exist
#      yet.  Their absence guarantees that later grading is unambiguous.

import json
from pathlib import Path

import pytest


LOG_DIR = Path("/home/user/logs")
COMBINED_LOG = LOG_DIR / "combined.log"

TRIAGE_DIR = Path("/home/user/incident_triage")
FILTERED_LOG = TRIAGE_DIR / "filtered_2023-10-12_1400-1415.log"
SUMMARY_TXT = TRIAGE_DIR / "error_summary.txt"

# The exact, line-for-line contents that must be present in combined.log
_EXPECTED_COMBINED_LOG = (
    '{"ts":"2023-10-12T13:58:44Z","level":"INFO","code":20000,"msg":"healthcheck ok"}\n'
    '{"ts":"2023-10-12T14:00:02Z","level":"WARN","code":49999,"msg":"slow response detected"}\n'
    '{"ts":"2023-10-12T14:01:19Z","level":"ERROR","code":50203,"msg":"upstream connection reset"}\n'
    '{"ts":"2023-10-12T14:03:11Z","level":"ERROR","code":50203,"msg":"upstream connection reset"}\n'
    '{"ts":"2023-10-12T14:04:23Z","level":"INFO","code":20000,"msg":"healthcheck ok"}\n'
    '{"ts":"2023-10-12T14:07:05Z","level":"WARN","code":40001,"msg":"client aborted request"}\n'
    '{"ts":"2023-10-12T14:10:42Z","level":"ERROR","code":50401,"msg":"gateway timeout"}\n'
    '{"ts":"2023-10-12T14:12:06Z","level":"ERROR","code":50203,"msg":"upstream connection reset"}\n'
    '{"ts":"2023-10-12T14:14:55Z","level":"WARN","code":49999,"msg":"slow response detected"}\n'
    '{"ts":"2023-10-12T14:16:03Z","level":"WARN","code":49999,"msg":"slow response detected"}\n'
    '{"ts":"2023-10-12T14:17:17Z","level":"ERROR","code":50401,"msg":"gateway timeout"}\n'
    '{"ts":"2023-10-12T14:20:00Z","level":"INFO","code":20000,"msg":"healthcheck ok"}\n'
    '{"ts":"2023-10-12T14:25:12Z","level":"ERROR","code":50401,"msg":"gateway timeout"}\n'
    '{"ts":"2023-10-12T14:31:30Z","level":"WARN","code":40001,"msg":"client aborted request"}\n'
    '{"ts":"2023-10-12T14:35:01Z","level":"INFO","code":20000,"msg":"healthcheck ok"}\n'
)


@pytest.mark.dependency(name="log_file_presence")
def test_log_directory_and_file_exist():
    """The /home/user/logs directory and combined.log file must exist."""
    assert LOG_DIR.is_dir(), f"Expected directory {LOG_DIR} to exist."
    assert COMBINED_LOG.is_file(), (
        f"Expected log file {COMBINED_LOG} to exist."
    )


@pytest.mark.dependency(depends=["log_file_presence"], name="log_file_content")
def test_combined_log_content():
    """combined.log must contain exactly the expected 15 newline-terminated lines."""
    content = COMBINED_LOG.read_text(encoding="utf-8")
    assert (
        content == _EXPECTED_COMBINED_LOG
    ), "The contents of combined.log do not match the expected initial fixture."

    # Additional sanity check: every line is valid JSON with required keys
    for idx, line in enumerate(content.splitlines()):
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            pytest.fail(f"Line {idx+1} in combined.log is not valid JSON: {exc}")
        for key in ("ts", "level", "code", "msg"):
            assert (
                key in record
            ), f"Line {idx+1} in combined.log is missing key '{key}'."


def _assert_absent(path: Path):
    """Helper: assert that a path does not exist, fail with a clear message."""
    assert not path.exists(), f"Did not expect {path} to exist before the student’s solution runs."


@pytest.mark.dependency(depends=["log_file_content"])
def test_output_files_absent_initially():
    """
    The artefacts that the student must create must NOT exist yet; otherwise
    we couldn't know if their solution created them.
    """
    # The triage directory itself may or may not exist, but if it does,
    # the target files must still be absent.
    if TRIAGE_DIR.exists():
        assert TRIAGE_DIR.is_dir(), f"{TRIAGE_DIR} exists but is not a directory."

    _assert_absent(FILTERED_LOG)
    _assert_absent(SUMMARY_TXT)