# test_initial_state.py
#
# This test-suite validates that the operating-system and filesystem
# are in the expected pristine state **before** the student starts
# working on the “Collect and Consolidate Simulated Edge-Node Metrics”
# exercise.
#
# Expectations for the initial state:
#
# 1. The metrics simulator is present at the prescribed locations and
#    each feed file contains exactly 12 non-empty lines.
# 2. No artefacts from the yet-to-be-executed tasks exist:
#       – /home/user/edge_monitoring/        (directory may not exist)
#       – /home/user/edge_monitoring/**/*    (any required output files)
#       – /home/user/edge_monitoring.tar.gz  (or similarly named files)
#
# When a test fails, the assertion message will explicitly tell the
# student what is missing or unexpected.


import os
from pathlib import Path

import pytest

# ----------------------------------------------------------------------
# CONSTANTS
# ----------------------------------------------------------------------

HOME = Path("/home/user")
SIM_ROOT = HOME / "iot_simulator"
SIM_NODES = ["nodeA", "nodeB", "nodeC"]
FEED_FILENAME = "metrics_feed"

WORK_DIR = HOME / "edge_monitoring"
OUTPUT_FILES = [
    WORK_DIR / "metrics_nodeA.log",
    WORK_DIR / "metrics_nodeB.log",
    WORK_DIR / "metrics_nodeC.log",
    WORK_DIR / "all_nodes_metrics.csv",
    WORK_DIR / "summary.txt",
]
TARBALL = HOME / "edge_monitoring" / "edge_metrics_20240501.tar.gz"

# ----------------------------------------------------------------------
# HELPERS
# ----------------------------------------------------------------------


def read_lines(path: Path):
    """Return a list of stripped lines from *path*."""
    with path.open("r", encoding="utf-8") as fh:
        return [line.rstrip("\n") for line in fh]


# ----------------------------------------------------------------------
# TESTS
# ----------------------------------------------------------------------


def test_simulator_directory_structure_exists():
    """The simulator root and per-node directories must exist."""
    assert SIM_ROOT.is_dir(), f"Simulator root missing: {SIM_ROOT}"
    for node in SIM_NODES:
        node_dir = SIM_ROOT / node
        assert node_dir.is_dir(), f"Missing simulator node directory: {node_dir}"


@pytest.mark.parametrize("node", SIM_NODES)
def test_feed_files_exist(node):
    """Each node must have its metrics_feed file in place."""
    feed_path = SIM_ROOT / node / FEED_FILENAME
    assert feed_path.is_file(), f"Expected feed file not found: {feed_path}"


@pytest.mark.parametrize("node", SIM_NODES)
def test_feed_files_have_exactly_12_lines(node):
    """Every feed file must contain exactly 12 non-blank lines."""
    feed_path = SIM_ROOT / node / FEED_FILENAME
    lines = read_lines(feed_path)
    assert (
        len(lines) == 12
    ), f"{feed_path} should have 12 lines, found {len(lines)} lines"
    # Ensure no blank lines (helps catch accidental trailing newlines).
    blank_count = sum(1 for ln in lines if ln.strip() == "")
    assert (
        blank_count == 0
    ), f"{feed_path} contains {blank_count} blank/whitespace-only lines"


@pytest.mark.parametrize("node", SIM_NODES)
def test_each_feed_line_has_nine_csv_fields(node):
    """Quick sanity check: each simulator line must have 9 comma-separated columns."""
    feed_path = SIM_ROOT / node / FEED_FILENAME
    for idx, line in enumerate(read_lines(feed_path), start=1):
        field_count = line.count(",") + 1 if line else 0
        assert (
            field_count == 9
        ), f"{feed_path}: line {idx} has {field_count} fields (expected 9)"


def test_work_directory_not_populated_yet():
    """
    Before the student starts, the output directory must not contain any
    of the final artefacts.  The directory itself may not exist at all.
    """
    if WORK_DIR.exists():
        assert (
            WORK_DIR.is_dir()
        ), f"{WORK_DIR} exists but is not a directory; please remove it and restart the exercise."

        unexpected_items = [
            str(p)
            for p in OUTPUT_FILES + [TARBALL]
            if p.exists()
        ]
        assert (
            not unexpected_items
        ), (
            "The following output files are present *before* the task has "
            f"begun and must be removed: {', '.join(unexpected_items)}"
        )
    else:
        # Directory is absent, which is acceptable for the starting state.
        assert True