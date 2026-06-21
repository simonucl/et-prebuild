# test_initial_state.py
"""
Pytest suite that validates the *initial* filesystem state before the student
script runs.

It deliberately checks ONLY the resources that are guaranteed to exist before
any work starts.  It does **not** test for the presence or absence of any
output files or directories created by the student solution.
"""

from pathlib import Path

# --------------------------------------------------------------------------- #
# Constants                                                                   #
# --------------------------------------------------------------------------- #

HOME = Path("/home/user")

RAW_RUN_DIR = HOME / "raw_runs" / "run_42"
METRICS_SOURCE_DIR = HOME / ".metrics_source"
EXPERIMENTS_DIR = HOME / "experiments"

MODEL_FILE = RAW_RUN_DIR / "model.pt"
METRICS_JSON_FILE = RAW_RUN_DIR / "metrics.json"
SIM_METRICS_CSV = METRICS_SOURCE_DIR / "sim_metrics.csv"

# Expected contents ---------------------------------------------------------- #

EXPECTED_CSV_LINES = [
    "23.1,45.2\n",
    "25.5,46.1\n",
    "26.3,47.0\n",
    "24.1,46.5\n",
    "22.8,45.9\n",
]

EXPECTED_METRICS_JSON_CONTENT = "{}\n"


# --------------------------------------------------------------------------- #
# Helper assertions                                                           #
# --------------------------------------------------------------------------- #

def assert_is_dir(path: Path):
    assert path.exists(), f"Required directory missing: {path}"
    assert path.is_dir(), f"Expected {path} to be a directory"


def assert_is_file(path: Path):
    assert path.exists(), f"Required file missing: {path}"
    assert path.is_file(), f"Expected {path} to be a regular file"


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #

def test_required_directories_exist():
    """
    The three pre-populated directories must be present before the task starts.
    """
    for d in (RAW_RUN_DIR, METRICS_SOURCE_DIR, EXPERIMENTS_DIR):
        assert_is_dir(d)


def test_raw_artifact_files_exist_and_intact():
    """
    The raw artifact files must still be located inside raw_runs/run_42
    and must be unmodified.
    """
    # model.pt ----------------------------------------------------------------
    assert_is_file(MODEL_FILE)
    size = MODEL_FILE.stat().st_size
    assert size == 0, (
        f"{MODEL_FILE} should be an empty placeholder file (0 bytes) "
        f"but is {size} bytes"
    )

    # metrics.json ------------------------------------------------------------
    assert_is_file(METRICS_JSON_FILE)
    content = METRICS_JSON_FILE.read_text(encoding="utf-8")
    assert content == EXPECTED_METRICS_JSON_CONTENT, (
        f"{METRICS_JSON_FILE} content mismatch.\n"
        f"Expected: {EXPECTED_METRICS_JSON_CONTENT!r}\n"
        f"Found:    {content!r}"
    )


def test_sim_metrics_csv_exists_and_has_expected_content():
    """
    The simulated metrics CSV file must exist and contain exactly the five
    expected utilisation pairs, in order, with a trailing newline on each line.
    """
    assert_is_file(SIM_METRICS_CSV)

    lines = SIM_METRICS_CSV.read_text(encoding="utf-8").splitlines(keepends=True)
    assert lines == EXPECTED_CSV_LINES, (
        f"{SIM_METRICS_CSV} content mismatch.\n"
        "Expected lines:\n"
        + "".join(EXPECTED_CSV_LINES)
        + "Found lines:\n"
        + "".join(lines)
    )