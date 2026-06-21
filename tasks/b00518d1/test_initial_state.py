# test_initial_state.py
#
# This test-suite verifies that the **initial** filesystem state is correct
# before the student begins the exercise.  It deliberately *does not* look
# for any output directories or files that the student is expected to create.
#
# Checked items:
#   • /home/user/ml_pipeline/raw directory exists.
#   • The two TSV files exist and have the exact, expected, TAB-separated
#     contents (header + 5 data rows each, in ascending event_id order).
#
# The tests fail with clear, actionable error messages if anything is missing
# or incorrect.
#
# NOTE: Only stdlib + pytest are used.

from pathlib import Path
import pytest

RAW_DIR = Path("/home/user/ml_pipeline/raw")
PART1_PATH = RAW_DIR / "user_events_part1.tsv"
PART2_PATH = RAW_DIR / "user_events_part2.tsv"

# Expected, canonical contents of the input TSV files.
PART1_EXPECTED_LINES = [
    "event_id\tuser_id\ttimestamp\tevent_type",
    "1\t1001\t2023-05-01T12:00:00Z\tclick",
    "2\t1002\t2023-05-01T12:05:00Z\tview",
    "3\t1003\t2023-05-01T12:10:00Z\tpurchase",
    "4\t1004\t2023-05-01T12:20:00Z\tclick",
    "5\t1005\t2023-05-01T12:25:00Z\tpurchase",
]

PART2_EXPECTED_LINES = [
    "event_id\tcountry\tdevice\trevenue",
    "1\tUS\tmobile\t0.00",
    "2\tCA\tdesktop\t0.00",
    "3\tUS\tmobile\t19.99",
    "4\tGB\ttablet\t0.00",
    "5\tCA\tmobile\t25.50",
]


def _read_lines(path: Path):
    """
    Helper that returns a list of lines without their trailing newlines.
    """
    with path.open("r", encoding="utf-8") as fh:
        # Strip the universal newline characters to make comparison cleaner.
        return [ln.rstrip("\r\n") for ln in fh.readlines()]


def test_raw_directory_exists():
    """The raw data directory must exist and be a directory."""
    assert RAW_DIR.exists(), f"Missing directory: {RAW_DIR}"
    assert RAW_DIR.is_dir(), f"Expected {RAW_DIR} to be a directory"


@pytest.mark.parametrize(
    "path,expected_lines",
    [
        (PART1_PATH, PART1_EXPECTED_LINES),
        (PART2_PATH, PART2_EXPECTED_LINES),
    ],
)
def test_raw_files_exist_and_contents_match(path: Path, expected_lines):
    """
    Verify that each raw TSV file exists, is a file, and its exact
    TAB-separated content matches the canonical truth.
    """
    # 1. Existence and type
    assert path.exists(), f"Missing file: {path}"
    assert path.is_file(), f"{path} exists but is not a regular file"

    # 2. Read & compare contents
    actual_lines = _read_lines(path)

    # Helpful diagnostics on mismatch
    if actual_lines != expected_lines:
        diff = [
            f"\nExpected line {idx + 1!r}: {exp!r}\n           "
            f"got {idx + 1!r}: {act!r}"
            for idx, (exp, act) in enumerate(
                zip(expected_lines, actual_lines), start=0
            )
            if exp != act
        ]
        extra_info = (
            f"\nFile has {len(actual_lines)} lines; expected {len(expected_lines)}."
        )
        raise AssertionError(
            f"Contents of {path} do not match expected fixture."
            + "".join(diff[:5])  # show first few differences
            + extra_info
        )

    # 3. Quick format sanity: every non-empty line must contain at least one TAB.
    for idx, line in enumerate(actual_lines, start=1):
        if line and "\t" not in line:
            pytest.fail(
                f"Line {idx} in {path} does not contain a TAB character: {line!r}"
            )