# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the operating-system
# environment **before** the student performs any action for the
# “network-traffic triage” task.
#
# It checks that:
#   • /home/user/logs/network_traffic.log exists and has the exact
#     11 expected lines (with trailing newlines).
#   • The derived metrics from that file match the ground-truth values
#     given in the assignment description.
#   • /home/user/logs/analysis/traffic_summary.txt does **not** yet exist,
#     because the student is supposed to create it.
#
# Only stdlib + pytest are used.

from pathlib import Path
import pytest

LOG_FILE = Path("/home/user/logs/network_traffic.log")
ANALYSIS_DIR = Path("/home/user/logs/analysis")
SUMMARY_FILE = ANALYSIS_DIR / "traffic_summary.txt"

EXPECTED_LINES = [
    "2024-05-01T10:00:01Z 192.168.1.10 -> 10.0.0.5 450\n",
    "2024-05-01T10:00:02Z 192.168.1.20 -> 10.0.0.5 1500\n",
    "2024-05-01T10:00:03Z 192.168.1.10 -> 10.0.0.5 600\n",
    "2024-05-01T10:00:04Z 192.168.1.30 -> 10.0.0.5 200\n",
    "2024-05-01T10:00:05Z 192.168.1.20 -> 10.0.0.5 700\n",
    "2024-05-01T10:00:06Z 192.168.1.20 -> 10.0.0.5 800\n",
    "2024-05-01T10:00:07Z 192.168.1.40 -> 10.0.0.5 50\n",
    "2024-05-01T10:00:08Z 192.168.1.30 -> 10.0.0.5 300\n",
    "2024-05-01T10:00:09Z 192.168.1.10 -> 10.0.0.5 200\n",
    "2024-05-01T10:00:10Z 192.168.1.50 -> 10.0.0.5 1000\n",
    "2024-05-01T10:00:11Z 192.168.1.20 -> 10.0.0.5 500\n",
]

GROUND_TRUTH_UNIQUE_IPS = 5
GROUND_TRUTH_TOTALS = {
    "192.168.1.20": 3500,
    "192.168.1.10": 1250,
    "192.168.1.50": 1000,
    "192.168.1.30":  500,
    "192.168.1.40":   50,
}
GROUND_TRUTH_TOP_3 = [
    ("192.168.1.20", 3500),
    ("192.168.1.10", 1250),
    ("192.168.1.50", 1000),
]


def test_log_file_exists():
    assert LOG_FILE.is_file(), (
        f"Required log file {LOG_FILE} is missing. "
        "The assignment cannot proceed without it."
    )


def test_log_file_exact_content():
    actual_lines = LOG_FILE.read_text().splitlines(keepends=True)
    assert actual_lines == EXPECTED_LINES, (
        f"{LOG_FILE} does not contain the expected 11 lines or has been modified.\n"
        f"Expected:\n{''.join(EXPECTED_LINES)}\n"
        f"Found:\n{''.join(actual_lines)}"
    )


def test_derived_metrics_from_log_file():
    """
    Re-compute unique source IPs and per-IP byte totals, then
    compare them to the truths supplied by the specification.
    """
    src_totals = {}
    with LOG_FILE.open() as fh:
        for line in fh:
            parts = line.strip().split()
            # Expected fixed format:
            # ISO-8601  SRC_IP  ->  DST_IP  BYTES
            if len(parts) != 5 or parts[2] != "->":
                pytest.fail(f"Line with unexpected format in {LOG_FILE}: {line!r}")
            src_ip, bytes_str = parts[1], parts[4]
            try:
                bytes_int = int(bytes_str)
            except ValueError:
                pytest.fail(f"Non-integer byte count in {LOG_FILE}: {bytes_str!r}")
            src_totals[src_ip] = src_totals.get(src_ip, 0) + bytes_int

    # Unique source IPs
    assert len(src_totals) == GROUND_TRUTH_UNIQUE_IPS, (
        "The number of unique source IPs in the log file deviates from the "
        f"ground-truth value {GROUND_TRUTH_UNIQUE_IPS}."
    )

    # Per-IP totals
    assert src_totals == GROUND_TRUTH_TOTALS, (
        "Per-IP byte totals in the log file do not match ground-truth values.\n"
        f"Expected: {GROUND_TRUTH_TOTALS}\nActual:   {src_totals}"
    )

    # Top-3 talkers
    top_3_actual = sorted(src_totals.items(), key=lambda kv: (-kv[1], kv[0]))[:3]
    assert top_3_actual == GROUND_TRUTH_TOP_3, (
        "Top-3 talkers calculated from the log file are incorrect.\n"
        f"Expected: {GROUND_TRUTH_TOP_3}\nActual:   {top_3_actual}"
    )


def test_summary_file_not_yet_present():
    """
    The student is supposed to *create* traffic_summary.txt.
    If it is already present, the starting state is wrong.
    """
    assert not SUMMARY_FILE.exists(), (
        f"{SUMMARY_FILE} already exists, but it should be created by the "
        "student as part of the exercise."
    )