# test_initial_state.py
#
# This pytest file validates that the *initial* on-disk structure and
# contents exactly match what the exercise description promises.
#
# IMPORTANT
# ---------
# * These tests purposefully do **NOT** look for the output directory
#   (/home/user/data/benchmark) or its file – that is the student’s job
#   to create later.
# * Only the standard library and pytest are used.

from pathlib import Path
import pytest

HOME = Path("/home/user")
RAW_ROOT = HOME / "data" / "raw"

# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------


def read_lines(path: Path):
    """
    Return a list of lines **including** their terminating '\n'.
    Raises a clear assertion error if the file cannot be read.
    """
    try:
        with path.open("r", encoding="utf-8") as fp:
            return fp.readlines()
    except FileNotFoundError as exc:
        pytest.fail(f"Expected file not found: {path} – {exc}")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Unable to read {path}: {exc}")


# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------

def test_raw_root_exists_and_is_dir():
    assert RAW_ROOT.is_dir(), (
        f"Required directory missing: {RAW_ROOT}\n"
        "Make sure the starting data has been copied to the correct location."
    )


@pytest.mark.parametrize(
    "dataset, expected_csv_map",
    [
        (
            "dataset_A",
            {
                "file1.csv": 5,
                "file2.csv": 8,
            },
        ),
        (
            "dataset_B",
            {
                "data.csv": 10,
            },
        ),
        (
            "dataset_C",
            {
                "part1.csv": 4,
                "part2.csv": 6,
                "part3.csv": 10,
            },
        ),
    ],
)
def test_dataset_structure_and_line_counts(dataset, expected_csv_map):
    """
    For each dataset directory:

    1. The directory exists.
    2. Exactly the expected CSV files are present (no more, no less).
    3. Each CSV file has the expected number of text lines.
    """
    dataset_dir = RAW_ROOT / dataset
    assert dataset_dir.is_dir(), (
        f"Dataset directory missing: {dataset_dir}\n"
        "The initial data hierarchy must be present before starting the task."
    )

    # ------------------------------------------------------------------
    # 1. Directory contains exactly the expected CSV files
    # ------------------------------------------------------------------
    found_csv_files = {p.name for p in dataset_dir.glob("*.csv")}
    expected_csv_files = set(expected_csv_map.keys())

    missing = expected_csv_files - found_csv_files
    extra = found_csv_files - expected_csv_files

    if missing:
        pytest.fail(
            f"Dataset {dataset} is incomplete.\n"
            f"Missing CSV file(s): {', '.join(sorted(missing))}"
        )
    if extra:
        pytest.fail(
            f"Dataset {dataset} contains unexpected CSV file(s): "
            f"{', '.join(sorted(extra))}"
        )

    # ------------------------------------------------------------------
    # 2. Every file has the expected number of lines
    # ------------------------------------------------------------------
    for csv_name, expected_line_count in expected_csv_map.items():
        csv_path = dataset_dir / csv_name
        lines = read_lines(csv_path)
        assert len(lines) == expected_line_count, (
            f"Line-count mismatch in {csv_path}.\n"
            f"Expected {expected_line_count} lines but found {len(lines)}."
        )