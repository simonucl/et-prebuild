# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state before the
# learner performs any action.  In particular it checks that the experiment
# artefact directory and its index file are present **exactly** as described
# in the task statement.

import os
import stat
import pytest

EXP_DIR = "/home/user/experiment_artifacts"
INDEX_FILE = os.path.join(EXP_DIR, "artifact_index.txt")

# The exact, byte-for-byte contents that must already be in artifact_index.txt
EXPECTED_INDEX_CONTENT = (
    "model_v1.bin\n"
    "metrics_v1.json\n"
    "model_v2.bin\n"
    "metrics_v2.json\n"
    "model_v2.bin\n"
    "logs_v2.txt\n"
    "model_v1.bin\n"
    "summary_v1.pdf\n"
    "metrics_v1.json\n"
    "logs_v2.txt\n"
    "model_v3.bin\n"
    "metrics_v3.json\n"
    "model_v3.bin\n"
    "model_v3.bin\n"
)


def test_experiment_directory_exists_and_has_correct_permissions():
    """The experiment_artifacts directory must exist and be readable/executable
    by everyone (mode 755)."""
    assert os.path.isdir(EXP_DIR), (
        f"Required directory {EXP_DIR!r} is missing or is not a directory."
    )

    dir_mode = stat.S_IMODE(os.stat(EXP_DIR).st_mode)
    expected_mode = 0o755
    assert (
        dir_mode == expected_mode
    ), f"Directory {EXP_DIR!r} permissions are {oct(dir_mode)}, expected {oct(expected_mode)}."


def test_index_file_exists_and_has_correct_permissions():
    """artifact_index.txt must exist, be a regular file, and world-readable
    (mode 644)."""
    assert os.path.isfile(INDEX_FILE), (
        f"Required file {INDEX_FILE!r} is missing or is not a regular file."
    )

    file_mode = stat.S_IMODE(os.stat(INDEX_FILE).st_mode)
    expected_mode = 0o644
    assert (
        file_mode == expected_mode
    ), f"File {INDEX_FILE!r} permissions are {oct(file_mode)}, expected {oct(expected_mode)}."


def test_index_file_contents_are_exact():
    """artifact_index.txt must contain the exact, canonical list of artefact
    filenames provided in the task description."""
    with open(INDEX_FILE, "r", encoding="utf-8") as fh:
        actual_content = fh.read()

    assert (
        actual_content == EXPECTED_INDEX_CONTENT
    ), (
        "The contents of artifact_index.txt do not match the expected initial "
        "fixture.\n\n"
        "Expected:\n"
        f"{EXPECTED_INDEX_CONTENT!r}\n\n"
        "Actual:\n"
        f"{actual_content!r}"
    )


def test_index_file_line_count():
    """Sanity check: the index file must contain exactly 14 non-empty lines."""
    lines = EXPECTED_INDEX_CONTENT.strip("\n").split("\n")
    assert len(lines) == 14, (
        "Internal error in test fixture: EXPECTED_INDEX_CONTENT should contain "
        "14 lines."
    )

    with open(INDEX_FILE, "r", encoding="utf-8") as fh:
        actual_lines = [ln.rstrip("\n") for ln in fh.readlines()]

    assert len(actual_lines) == 14, (
        f"artifact_index.txt should have 14 lines, found {len(actual_lines)}."
    )