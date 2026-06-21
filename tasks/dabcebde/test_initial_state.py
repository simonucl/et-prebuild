# test_initial_state.py
#
# This pytest file validates that the machine starts in the *expected* state
# before the student runs any commands.  If any of these tests fail, the
# grading environment itself is not in the correct initial configuration.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user").resolve()

# ---------------------------------------------------------------------------
# Expected paths
# ---------------------------------------------------------------------------

SRC_ROOT            = HOME / "mlops/experiments/exp123"
SRC_METRICS_JSON    = SRC_ROOT / "metrics.json"
SRC_MODEL_PKL       = SRC_ROOT / "model.pkl"
SRC_LOGS_DIR        = SRC_ROOT / "logs"
SRC_TRAIN_LOG       = SRC_LOGS_DIR / "train.log"

DEST_ROOT           = HOME / "remote_server/exp_artifacts/exp123"
SYNC_LOGS_DIR       = HOME / "sync_logs"
SYNC_LOG_FILE       = SYNC_LOGS_DIR / "exp123_sync.log"

# ---------------------------------------------------------------------------
# Expected *exact* file contents
# ---------------------------------------------------------------------------

EXPECTED_METRICS_CONTENT = '{"accuracy": 0.92, "loss": 0.21}\n'
EXPECTED_MODEL_CONTENT   = b'DUMMY_MODEL_BINARY_CONTENT\n'
EXPECTED_TRAINLOG_CONTENT = (
    "Epoch 1/5 – loss:0.34 – acc:0.78\n"
    "Epoch 5/5 – loss:0.21 – acc:0.92\n"
)

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _assert_only_these_paths_exist(root: Path, expected_rel_paths):
    """
    Recursively walk 'root' and assert that the set of *relative* paths found
    matches 'expected_rel_paths' exactly (no more, no less).
    """
    found_paths = []
    for dirpath, dirnames, filenames in os.walk(root):
        prefix = Path(dirpath).relative_to(root)
        # Add directories (except root) to the list
        for d in dirnames:
            rel = (prefix / d)
            found_paths.append(rel.as_posix() + "/")
        # Add files
        for f in filenames:
            rel = (prefix / f)
            found_paths.append(rel.as_posix())
    assert set(found_paths) == set(expected_rel_paths), (
        f"Unexpected directory contents under {root}.\n"
        f"Expected: {sorted(expected_rel_paths)}\n"
        f"Found:    {sorted(found_paths)}"
    )

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_source_directory_structure_and_contents():
    """Source tree must exist and contain the three expected artefacts only."""
    assert SRC_ROOT.is_dir(), f"Source directory {SRC_ROOT} is missing."

    # Verify directory tree (include trailing slash for directories)
    expected_structure = [
        "metrics.json",
        "model.pkl",
        "logs/",            # directory
        "logs/train.log",
    ]
    _assert_only_these_paths_exist(SRC_ROOT, expected_structure)

    # metrics.json (text)
    assert SRC_METRICS_JSON.is_file(), f"{SRC_METRICS_JSON} not found."
    contents = SRC_METRICS_JSON.read_text(encoding="utf-8")
    assert contents == EXPECTED_METRICS_CONTENT, (
        f"{SRC_METRICS_JSON} content mismatch.\n"
        f"Expected: {EXPECTED_METRICS_CONTENT!r}\n"
        f"Found:    {contents!r}"
    )

    # model.pkl (binary)
    assert SRC_MODEL_PKL.is_file(), f"{SRC_MODEL_PKL} not found."
    bin_contents = SRC_MODEL_PKL.read_bytes()
    assert bin_contents == EXPECTED_MODEL_CONTENT, (
        f"{SRC_MODEL_PKL} content mismatch.\n"
        f"Expected bytes: {EXPECTED_MODEL_CONTENT!r}\n"
        f"Found bytes:    {bin_contents!r}"
    )

    # logs/train.log (text)
    assert SRC_TRAIN_LOG.is_file(), f"{SRC_TRAIN_LOG} not found."
    train_log_text = SRC_TRAIN_LOG.read_text(encoding="utf-8")
    assert train_log_text == EXPECTED_TRAINLOG_CONTENT, (
        f"{SRC_TRAIN_LOG} content mismatch.\n"
        f"Expected: {EXPECTED_TRAINLOG_CONTENT!r}\n"
        f"Found:    {train_log_text!r}"
    )

def test_destination_directory_is_empty():
    """Destination directory exists but is completely empty."""
    assert DEST_ROOT.is_dir(), f"Destination directory {DEST_ROOT} is missing."
    entries = list(DEST_ROOT.iterdir())
    assert not entries, (
        f"Destination directory {DEST_ROOT} should be empty but contains: "
        f"{[p.name for p in entries]}"
    )

def test_no_sync_logs_directory_yet():
    """The /home/user/sync_logs directory must not exist before the task."""
    assert not SYNC_LOGS_DIR.exists(), (
        f"{SYNC_LOGS_DIR} should NOT exist before synchronisation starts."
    )