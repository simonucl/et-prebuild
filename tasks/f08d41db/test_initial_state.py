# test_initial_state.py
#
# This pytest suite validates the *initial* operating-system / filesystem
# state for the “accuracy comparison” exercise.  It confirms that the two
# metric source files are present and correctly formatted **before** the
# student generates the report.  Nothing in here checks for the presence of
# the output directory or report file, in accordance with the grading rules.

import os
import pathlib
import pytest

HOME = pathlib.Path("/home/user")
ARTIFACTS_DIR = HOME / "mlops" / "artifacts" / "experiments"
ALPHA_FILE = ARTIFACTS_DIR / "alpha_metrics.tsv"
BETA_FILE = ARTIFACTS_DIR / "beta_metrics.tsv"

@pytest.mark.parametrize(
    "path",
    [ARTIFACTS_DIR, ALPHA_FILE, BETA_FILE],
)
def test_artifacts_exist(path):
    """
    The experiments directory and the two metrics files must exist.
    """
    assert path.exists(), f"Expected '{path}' to exist, but it is missing."
    if path in (ALPHA_FILE, BETA_FILE):
        assert path.is_file(), f"Expected '{path}' to be a file."


@pytest.mark.parametrize(
    "file_path, expected_header",
    [
        (
            ALPHA_FILE,
            ["epoch", "run_id", "alpha_acc", "alpha_loss"],
        ),
        (
            BETA_FILE,
            ["epoch", "run_id", "beta_acc", "beta_loss"],
        ),
    ],
)
def test_file_structure_and_header(file_path, expected_header):
    """
    Each metrics file must:
    • contain exactly 4 non-empty lines (1 header + 3 data rows);
    • be tab-separated, with exactly 4 columns per line;
    • have the exact expected header row.
    """
    with file_path.open("r", encoding="utf-8") as fh:
        raw_lines = fh.readlines()

    # Remove any trailing empty lines caused by extra newlines.
    lines = [ln for ln in raw_lines if ln.strip() != ""]

    # 1. Exactly 4 non-blank lines.
    assert len(lines) == 4, (
        f"File '{file_path}' should contain exactly 4 non-empty lines "
        f"(1 header + 3 data rows), but it contains {len(lines)}."
    )

    # 2. Each line must end with a single LF newline character.
    for idx, ln in enumerate(raw_lines, start=1):
        assert ln.endswith("\n"), (
            f"Line {idx} in '{file_path}' does not end with a single LF newline."
        )

    # 3. Validate header row.
    header_columns = lines[0].rstrip("\n").split("\t")
    assert header_columns == expected_header, (
        f"Header in '{file_path}' is incorrect.\n"
        f"Expected: {expected_header}\n"
        f"Found   : {header_columns}"
    )

    # 4. Validate each data row has 4 tab-separated columns.
    for line_num, data_line in enumerate(lines[1:], start=2):  # start=2 for human-friendly line numbers
        cols = data_line.rstrip("\n").split("\t")
        assert len(cols) == 4, (
            f"Line {line_num} in '{file_path}' should have 4 tab-separated "
            f"columns, but it has {len(cols)} columns: {cols}"
        )
        # First column must be an integer epoch number 1-3.
        try:
            epoch_val = int(cols[0])
        except ValueError:
            pytest.fail(
                f"First column of line {line_num} in '{file_path}' should be an "
                f"integer epoch number, but found '{cols[0]}'."
            )
        assert epoch_val in {1, 2, 3}, (
            f"Epoch value in line {line_num} of '{file_path}' should be 1, 2 or 3, "
            f"but found {epoch_val}."
        )