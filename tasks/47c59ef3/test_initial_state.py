# test_initial_state.py
#
# This pytest suite verifies the **initial** filesystem state for the
# “component metadata clean-up” exercise.  It intentionally checks ONLY the
# input artefacts that must exist *before* the student performs any work.
# It does **not** look for, or impose requirements on, the files that the
# student is expected to create (`combined_components.tsv`,
# `process.log`, etc.).
#
# The tests confirm:
#   • /home/user/project exists and is a directory.
#   • component_a.tsv   exists, is readable, and contains the exact
#     3-column, tab-separated contents described in the spec.
#   • component_b.tsv   exists, is readable, and contains the exact
#     2-column, tab-separated contents described in the spec.
#
# If any of these checks fail, the error messages are explicit so that the
# learner (or course maintainer) can quickly see what prerequisite piece is
# missing or malformed.

import os
from pathlib import Path

import pytest

PROJECT_DIR = Path("/home/user/project")
COMP_A = PROJECT_DIR / "component_a.tsv"
COMP_B = PROJECT_DIR / "component_b.tsv"

EXPECTED_A_CONTENT = (
    "comp_login\tv1.2\talice\n"
    "comp_payments\tv2.0\tbob\n"
    "comp_notifications\tv1.4\tcarol\n"
    "comp_search\tv1.8\tdave\n"
)
EXPECTED_B_CONTENT = (
    "comp_login\tstable\n"
    "comp_payments\tdeprecated\n"
    "comp_notifications\tbeta\n"
    "comp_search\tstable\n"
)


def _read_text(path: Path) -> str:
    """Read file as UTF-8 text; raise an explicit failure if unreadable."""
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read {path}: {exc}")


def test_project_directory_exists():
    assert PROJECT_DIR.exists(), f"Required directory {PROJECT_DIR} is missing."
    assert PROJECT_DIR.is_dir(), f"{PROJECT_DIR} exists but is not a directory."


@pytest.mark.parametrize(
    "path, expected, ncols",
    [
        (COMP_A, EXPECTED_A_CONTENT, 3),
        (COMP_B, EXPECTED_B_CONTENT, 2),
    ],
)
def test_tsv_files_present_and_correct(path: Path, expected: str, ncols: int):
    assert path.exists(), f"Required file {path} is missing."
    assert path.is_file(), f"{path} exists but is not a regular file."

    text = _read_text(path)

    # 1) Exact byte-for-byte match to the canonical contents
    assert (
        text == expected
    ), f"Contents of {path} do not match the expected initial dataset."

    # 2) Defensive checks: correct trailing newline and column counts
    assert text.endswith(
        "\n"
    ), f"{path} must end with a single Unix newline (\\n)."

    lines = text.rstrip("\n").split("\n")
    assert len(lines) == 4, f"{path} should have exactly 4 data lines."

    for idx, line in enumerate(lines, start=1):
        cols = line.split("\t")
        assert (
            len(cols) == ncols
        ), f"Line {idx} in {path} should have {ncols} tab-separated columns, got {len(cols)}."