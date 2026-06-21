# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / file-system
# state before the student carries out any actions for the
# “Kubernetes Operator – Concurrent Apply Benchmark & Manifest Metrics” task.
#
# Requirements being validated:
#   1. The three manifest files must already exist with the exact, expected
#      number of non-blank lines.
#   2. No benchmark artefacts created by the student should be present yet.
#
# Only stdlib + pytest are used.

from pathlib import Path
import pytest

HOME = Path("/home/user")

MANIFEST_DIR = HOME / "manifests"
BENCHMARK_DIR = HOME / "benchmark"

MANIFEST_FILES = {
    "deployment": MANIFEST_DIR / "deployment.yaml",
    "service": MANIFEST_DIR / "service.yaml",
    "configmap": MANIFEST_DIR / "configmap.yaml",
}

# Expected non-blank line counts taken from the fixture in the task description
EXPECTED_LINE_COUNTS = {
    "deployment": 19,
    "service": 11,
    "configmap": 7,
    "total": 37,
}

BENCHMARK_ARTIFACTS = {
    "json_report": BENCHMARK_DIR / "operator_benchmark.json",
    "log_file": BENCHMARK_DIR / "parallel_commands_executed.log",
}


# --------------------------------------------------------------------------- #
# Helper
# --------------------------------------------------------------------------- #
def _non_blank_line_count(path: Path) -> int:
    """Return the count of non-blank lines in a text file."""
    with path.open(encoding="utf-8") as fh:
        return sum(1 for line in fh if line.strip())


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_manifests_directory_exists():
    assert MANIFEST_DIR.is_dir(), (
        f"Expected directory '{MANIFEST_DIR}' missing. "
        "The provided manifests must live here before you start the task."
    )


@pytest.mark.parametrize("key", ["deployment", "service", "configmap"])
def test_each_manifest_exists(key):
    path = MANIFEST_FILES[key]
    assert path.is_file(), (
        f"Manifest '{path}' is missing. "
        "The automated environment should already contain this file."
    )


@pytest.mark.parametrize(
    "key,expected",
    [
        ("deployment", EXPECTED_LINE_COUNTS["deployment"]),
        ("service", EXPECTED_LINE_COUNTS["service"]),
        ("configmap", EXPECTED_LINE_COUNTS["configmap"]),
    ],
)
def test_manifest_line_counts(key, expected):
    """
    Ensure each manifest has the exact number of non-blank lines
    stated in the task description. This guarantees that students
    compute identical metrics later on.
    """
    path = MANIFEST_FILES[key]
    actual = _non_blank_line_count(path)
    assert actual == expected, (
        f"Manifest '{path}' has {actual} non-blank lines; "
        f"expected {expected}. File contents appear to have changed."
    )


def test_combined_manifest_line_count():
    total = sum(_non_blank_line_count(p) for p in MANIFEST_FILES.values())
    expected_total = EXPECTED_LINE_COUNTS["total"]
    assert total == expected_total, (
        f"Combined non-blank line count is {total}; expected {expected_total}. "
        "At least one manifest file differs from the expected fixture."
    )


def test_no_benchmark_artefacts_yet():
    """
    Before the student begins, the benchmark directory should *not* contain
    the artefacts that the assignment asks them to create.
    """
    for artefact_name, artefact_path in BENCHMARK_ARTIFACTS.items():
        assert not artefact_path.exists(), (
            f"Unexpected file '{artefact_path}' already exists. "
            "The student has not yet run the benchmark steps, so this file "
            f"must be absent at the initial state ({artefact_name})."
        )