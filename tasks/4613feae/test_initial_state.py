# test_initial_state.py
#
# This pytest suite validates the *initial* state of the operating system
# before the student writes and executes any script.  It deliberately checks
# only the pre-existing files that the assignment guarantees to be present and
# does *not* touch the output artefacts the student is asked to create later
# (e.g. summary CSV, archived configs, or the Bash script itself).
#
# If any of these tests fail, the student’s workspace is incomplete or has been
# modified in an unexpected way.

import json
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants describing the required initial filesystem layout and contents
# ---------------------------------------------------------------------------

BASE_DIR = Path("/home/user/mlops")
EXP_DIR = BASE_DIR / "experiments"

RUN_001_DIR = EXP_DIR / "run_001"
RUN_002_DIR = EXP_DIR / "run_002"

FILES_EXPECTED = {
    RUN_001_DIR / "config.json": (
        '{"lr":0.001,"batch_size":32,"optimizer":"adam"}',
        "config.json for run_001",
    ),
    RUN_001_DIR / "metrics.json": (
        '{"accuracy":0.92,"loss":0.35}',
        "metrics.json for run_001",
    ),
    RUN_002_DIR / "config.json": (
        '{"lr":0.0005,"batch_size":16,"optimizer":"sgd"}',
        "config.json for run_002",
    ),
    RUN_002_DIR / "metrics.json": (
        '{"accuracy":0.88,"loss":0.42}',
        "metrics.json for run_002",
    ),
}


# ---------------------------------------------------------------------------
# Helper Utilities
# ---------------------------------------------------------------------------


def _load_file_strip_newline(path: Path) -> str:
    """
    Read entire file, strip a single trailing newline (LF) if present,
    and return the content *exactly* as it should appear for comparison.
    """
    with path.open("r", encoding="utf-8") as fh:
        contents = fh.read()
    # Allow either presence or absence of exactly one trailing newline
    if contents.endswith("\n"):
        contents = contents[:-1]
    return contents


# ---------------------------------------------------------------------------
# Pytest Test Cases
# ---------------------------------------------------------------------------


def test_experiments_directory_exists():
    assert EXP_DIR.is_dir(), (
        f"Required directory {EXP_DIR} is missing. "
        "The repository should contain the 'experiments' folder with sample runs."
    )


def test_run_directories_exist():
    for run_dir in (RUN_001_DIR, RUN_002_DIR):
        assert run_dir.is_dir(), f"Expected run directory {run_dir} to exist."


def test_expected_files_exist_and_have_exact_contents():
    """
    Verify that each expected file exists **and** contains the exact one-line
    JSON string provided in the assignment (no extra spaces or reordered keys).
    """
    for path, (expected_content, human_name) in FILES_EXPECTED.items():
        assert path.is_file(), f"Missing {human_name} at {path}."

        actual_content = _load_file_strip_newline(path)
        assert (
            actual_content == expected_content
        ), f"Content mismatch in {human_name} ({path})."


def test_metrics_json_parses_and_has_expected_fields():
    """
    Parsing the metrics.json files confirms they are valid JSON and contain the
    required numeric keys 'accuracy' and 'loss' with the correct values.
    """
    expected_values = {
        RUN_001_DIR / "metrics.json": {"accuracy": 0.92, "loss": 0.35},
        RUN_002_DIR / "metrics.json": {"accuracy": 0.88, "loss": 0.42},
    }

    for path, expected in expected_values.items():
        # File existence already checked in previous test; re-read for clarity
        data = json.loads(path.read_text(encoding="utf-8").strip())
        assert (
            "accuracy" in data and "loss" in data
        ), f"{path} should contain 'accuracy' and 'loss' keys."

        for key, value in expected.items():
            assert (
                data.get(key) == value
            ), f"{path}: Expected {key}={value}, found {data.get(key)}."