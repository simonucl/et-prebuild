# test_initial_state.py
#
# Pytest suite to validate the **initial** filesystem state for the
# “experiment tracking” task _before_ the student performs any action.
#
# Expectations (truth values):
#   • /home/user/experiments exists and is a directory.
#   • /home/user/experiments/experiment_metrics.csv
#       - Exists.
#       - Uses LF (Unix) line endings only.
#       - Contains exactly:
#           experiment_id,accuracy,loss\n
#           1,0.85,0.45\n
#           2,0.88,0.40\n
#   • /home/user/experiments/last_run_config.json
#       - Exists.
#       - Single-line JSON: {"lr":0.001,"accuracy":0.93,"loss":0.35}
#       - No trailing newline (i.e., the file has zero “\n” bytes).
#   • /home/user/experiments/best_accuracy.json  MUST NOT exist yet.
#   • /home/user/experiments/update_log.txt      MUST NOT exist yet.
#
# Only Python stdlib + pytest are used.

import os
import pathlib
import pytest

HOME = pathlib.Path("/home/user")
EXP_DIR = HOME / "experiments"

CSV_PATH = EXP_DIR / "experiment_metrics.csv"
JSON_PATH = EXP_DIR / "last_run_config.json"
BEST_JSON_PATH = EXP_DIR / "best_accuracy.json"
LOG_PATH = EXP_DIR / "update_log.txt"


def _read_binary(path: pathlib.Path) -> bytes:
    """Read file as bytes; raise helpful assertion if file missing."""
    assert path.exists(), f"Expected file '{path}' is missing."
    return path.read_bytes()


def test_experiments_directory_exists():
    assert EXP_DIR.exists(), f"Directory {EXP_DIR} does not exist."
    assert EXP_DIR.is_dir(), f"{EXP_DIR} exists but is not a directory."


def test_experiment_metrics_csv_initial_contents():
    expected = (
        b"experiment_id,accuracy,loss\n"
        b"1,0.85,0.45\n"
        b"2,0.88,0.40\n"
    )
    data = _read_binary(CSV_PATH)

    # 1) Verify exact content.
    assert (
        data == expected
    ), (
        f"{CSV_PATH} does not contain the expected initial CSV data.\n"
        f"Expected bytes:\n{expected!r}\n\nActual bytes:\n{data!r}"
    )

    # 2) Ensure only LF line endings (no CR).
    assert b"\r" not in data, (
        f"{CSV_PATH} contains CR characters; only Unix LF line endings are allowed."
    )


def test_last_run_config_json_initial_contents():
    expected = b'{"lr":0.001,"accuracy":0.93,"loss":0.35}'
    data = _read_binary(JSON_PATH)

    # Must match exactly (no extra spaces, no pretty printing).
    assert (
        data == expected
    ), (
        f"{JSON_PATH} does not match the expected single-line JSON content.\n"
        f"Expected bytes:\n{expected!r}\n\nActual bytes:\n{data!r}"
    )

    # Must be one single line (no newline characters at all).
    assert b"\n" not in data, (
        f"{JSON_PATH} must be a single line with no newline character."
    )
    assert b"\r" not in data, (
        f"{JSON_PATH} contains CR characters; only a single line with no newline is expected."
    )


@pytest.mark.parametrize(
    "path",
    [
        BEST_JSON_PATH,
        LOG_PATH,
    ],
)
def test_output_files_do_not_exist_yet(path: pathlib.Path):
    assert (
        not path.exists()
    ), f"Output file '{path}' should NOT exist prior to performing the task."