# test_initial_state.py
#
# This pytest suite validates that the *initial* filesystem state
# is correct **before** the student starts working on the task.
#
# What we check:
#   1. The two raw, tab-separated source files exist at their full paths.
#   2. Their contents are byte-for-byte identical to the specification.
#
# What we explicitly do NOT check (in accordance with the rules):
#   • The presence or absence of any output/processed files or directories.
#
# Only Python’s standard library and pytest are used.

from pathlib import Path
import pytest

# ---------------------------------------------------------------------------
# Constants – expected file paths and their exact contents                   |
# ---------------------------------------------------------------------------

RAW_DIR = Path("/home/user/data/raw")

USER_FEATURES_PATH = RAW_DIR / "user_features.tsv"
ACTIVITY_STATS_PATH = RAW_DIR / "activity_stats.tsv"

EXPECTED_USER_FEATURES = (
    "id\tage\theight_cm\tweight_kg\n"
    "1\t25\t175\t70\n"
    "2\t31\t168\t80\n"
    "3\t22\t180\t75\n"
)

EXPECTED_ACTIVITY_STATS = (
    "id\tavg_daily_steps\tmax_heart_rate\n"
    "1\t8000\t190\n"
    "2\t6500\t180\n"
    "3\t12000\t200\n"
)


# ---------------------------------------------------------------------------
# Helper utilities                                                           |
# ---------------------------------------------------------------------------

def _read_text(path: Path) -> str:
    """
    Read a text file using UTF-8 encoding.
    Provides a clear pytest assertion message on failure.
    """
    if not path.exists():
        pytest.fail(f"Expected file does not exist: {path}")
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read {path}: {exc}")


# ---------------------------------------------------------------------------
# Tests                                                                      |
# ---------------------------------------------------------------------------

def test_user_features_file_exists_and_is_correct():
    """
    The raw user_features.tsv must exist and match the exact expected content.
    """
    actual_content = _read_text(USER_FEATURES_PATH)
    assert actual_content == EXPECTED_USER_FEATURES, (
        f"Content mismatch for {USER_FEATURES_PATH}\n"
        f"Expected:\n{EXPECTED_USER_FEATURES!r}\n\n"
        f"Got:\n{actual_content!r}"
    )


def test_activity_stats_file_exists_and_is_correct():
    """
    The raw activity_stats.tsv must exist and match the exact expected content.
    """
    actual_content = _read_text(ACTIVITY_STATS_PATH)
    assert actual_content == EXPECTED_ACTIVITY_STATS, (
        f"Content mismatch for {ACTIVITY_STATS_PATH}\n"
        f"Expected:\n{EXPECTED_ACTIVITY_STATS!r}\n\n"
        f"Got:\n{actual_content!r}"
    )