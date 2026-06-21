# test_initial_state.py
#
# This pytest suite verifies that the operating-system / filesystem
# is in the pristine “before the student starts” state.
#
# It asserts that:
#   1.  The raw trace file /home/user/logs/perf_data.log exists and its
#       contents exactly match the 10 reference lines (including spacing
#       and trailing newlines).
#   2.  None of the output artefacts that the student is supposed to
#       create yet exist:
#           • /home/user/reports/ (directory)
#           • /home/user/reports/perf_summary.csv
#           • /home/user/reports/max_latency.log
#           • /home/user/logs/perf_data_sanitized.log
#
# If any assertion fails, the error message pinpoints the mismatch so
# the learner immediately sees what is wrong.

from pathlib import Path
import difflib
import pytest

# --------------------------------------------------------------------
# Constants for paths we will examine
# --------------------------------------------------------------------
RAW_LOG_PATH = Path("/home/user/logs/perf_data.log")

REPORTS_DIR   = Path("/home/user/reports")
SUMMARY_CSV   = REPORTS_DIR / "perf_summary.csv"
MAX_LATENCY   = REPORTS_DIR / "max_latency.log"
SANITIZED_LOG = Path("/home/user/logs/perf_data_sanitized.log")

# --------------------------------------------------------------------
# The 10 exact reference lines (LF terminated) that must be present
# in /home/user/logs/perf_data.log before any work starts.
# Be careful to preserve double-spaces where they appear in the
# original specification (lines 5 and 9).
# --------------------------------------------------------------------
EXPECTED_RAW_LINES = [
    "2023-07-01T12:00:01Z appX latency_ms=123 cpu_pct=45.6 mem_mb=256\n",
    "2023-07-01T12:00:02Z appY latency_ms=200 cpu_pct=78.9 mem_mb=512\n",
    "2023-07-01T12:00:03Z appX latency_ms=150 cpu_pct=50.1 mem_mb=260\n",
    "2023-07-01T12:00:04Z appY latency_ms=180 cpu_pct=70.3 mem_mb=500\n",
    "2023-07-01T12:00:05Z appZ latency_ms=95  cpu_pct=30.0 mem_mb=128\n",
    "2023-07-01T12:00:06Z appX latency_ms=110 cpu_pct=40.0 mem_mb=255\n",
    "2023-07-01T12:00:07Z appZ latency_ms=105 cpu_pct=32.5 mem_mb=130\n",
    "2023-07-01T12:00:08Z appY latency_ms=250 cpu_pct=85.0 mem_mb=520\n",
    "2023-07-01T12:00:09Z appZ latency_ms=90  cpu_pct=29.5 mem_mb=127\n",
    "2023-07-01T12:00:10Z appX latency_ms=200 cpu_pct=60.0 mem_mb=300\n",
]

# --------------------------------------------------------------------
# Helper
# --------------------------------------------------------------------
def _pretty_diff(expected: list[str], actual: list[str]) -> str:
    """
    Produce a unified diff that highlights any discrepancy between
    expected and actual file contents.
    """
    return "\n".join(
        difflib.unified_diff(
            expected,
            actual,
            fromfile="expected",
            tofile="actual",
            lineterm=""
        )
    )

# --------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------
def test_raw_log_exists_and_matches_expected_contents():
    """Verify that the raw performance log exists and is byte-perfect."""
    assert RAW_LOG_PATH.is_file(), (
        f"Required input file {RAW_LOG_PATH} is missing."
    )

    # Read as text; the default encoding (utf-8) is sufficient here.
    with RAW_LOG_PATH.open("r", encoding="utf-8", newline="") as fh:
        actual_lines = fh.readlines()

    # 1) Correct number of lines
    assert len(actual_lines) == 10, (
        f"{RAW_LOG_PATH} should contain exactly 10 lines, "
        f"but has {len(actual_lines)}."
    )

    # 2) Exact byte-for-byte match (incl. white-space & newlines)
    if actual_lines != EXPECTED_RAW_LINES:
        diff = _pretty_diff(EXPECTED_RAW_LINES, actual_lines)
        pytest.fail(
            "Contents of /home/user/logs/perf_data.log do not match the "
            "expected reference. Diff (expected ↔ actual):\n\n" + diff
        )

@pytest.mark.parametrize(
    "path",
    [
        REPORTS_DIR,
        SUMMARY_CSV,
        MAX_LATENCY,
        SANITIZED_LOG,
    ],
)
def test_output_paths_do_not_exist_yet(path: Path):
    """
    Before the student runs their solution, none of the output artefact
    paths (nor even the reports directory) should exist.  Their presence
    would indicate that the environment is already ‘tainted’.
    """
    assert not path.exists(), (
        f"Path {path} exists before the exercise starts, but it should "
        f"only be created by the learner’s solution."
    )