# test_initial_state.py
#
# Pytest suite that verifies the operating-system / filesystem state
# *before* the student performs any actions for the “sensor log” task.
#
# Rules fulfilled:
#   • Uses only stdlib + pytest
#   • Checks absolute paths only
#   • Does NOT touch or test for any of the expected output artefacts
#     (/home/user/output, failures_2023.log, failures_count.txt, …)

import io
from pathlib import Path

DATA_DIR = Path("/home/user/data")
LOG_FILE = DATA_DIR / "sensor_readings_2023.log"

# Exact content that must already be present in the raw log file.
EXPECTED_LINES = [
    "2023-06-01T00:00:01Z SENSOR_ID=alpha STATUS=OK   TEMP=24.5C HUM=45%",
    "2023-06-01T00:30:01Z SENSOR_ID=alpha STATUS=FAIL TEMP=0.0C  HUM=0%",
    "2023-06-01T01:00:01Z SENSOR_ID=beta  STATUS=OK   TEMP=23.1C HUM=47%",
    "2023-06-01T01:30:01Z SENSOR_ID=beta  STATUS=FAIL TEMP=-5.0C HUM=0%",
    "2023-06-01T02:00:01Z SENSOR_ID=gamma STATUS=OK   TEMP=22.8C HUM=44%",
    "2023-06-01T02:30:01Z SENSOR_ID=gamma STATUS=OK   TEMP=22.9C HUM=44%",
    "2023-06-01T03:00:01Z SENSOR_ID=alpha STATUS=OK   TEMP=24.7C HUM=45%",
    "2023-06-01T03:30:01Z SENSOR_ID=beta  STATUS=OK   TEMP=23.4C HUM=47%",
    "2023-06-01T04:00:01Z SENSOR_ID=gamma STATUS=FAIL TEMP=-10.0C HUM=0%",
    "2023-06-01T04:30:01Z SENSOR_ID=alpha STATUS=OK   TEMP=24.6C HUM=46%",
]


def test_data_directory_exists():
    assert DATA_DIR.exists(), f"Required directory {DATA_DIR} is missing."
    assert DATA_DIR.is_dir(), f"{DATA_DIR} exists but is not a directory."


def test_log_file_exists():
    assert LOG_FILE.exists(), f"Required log file {LOG_FILE} is missing."
    assert LOG_FILE.is_file(), f"{LOG_FILE} exists but is not a regular file."


def test_log_file_contents_and_encoding():
    """
    The file must be valid UTF-8, contain exactly 10 lines,
    and match the expected byte-for-byte content (excluding the final newline
    which is acceptable but not required on the very last line).
    """
    # Read in binary then decode so we fail if encoding is wrong.
    raw_bytes = LOG_FILE.read_bytes()

    try:
        text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise AssertionError(
            f"{LOG_FILE} is not valid UTF-8: {exc}"
        ) from exc

    # Preserve trailing newline information
    buffer = io.StringIO(text)
    lines = [ln.rstrip("\n") for ln in buffer.readlines()]

    assert (
        len(lines) == 10
    ), f"{LOG_FILE} should contain exactly 10 lines, found {len(lines)}."

    # Compare each line so differences are easy to spot.
    mismatches = [
        (i + 1, exp, got)
        for i, (exp, got) in enumerate(zip(EXPECTED_LINES, lines))
        if exp != got
    ]
    if mismatches:
        msg_lines = [
            f"Line {idx}: expected:\n    {exp}\n  got:\n    {got}"
            for idx, exp, got in mismatches
        ]
        raise AssertionError(
            f"{LOG_FILE} content does not match expected:\n" + "\n".join(msg_lines)
        )