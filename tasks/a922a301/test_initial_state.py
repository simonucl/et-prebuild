# test_initial_state.py
#
# Pytest suite that validates the initial on-disk state *before* the student
# starts working on the assignment.  It checks that the fixture CSV files are
# present, contain the expected data, and that no additional “build_*.csv”
# files are lurking in /home/user/ci_metrics.
#
# NOTE: Per the project guidelines we intentionally do **not** inspect or even
# mention any of the *output* artefacts that the student is supposed to create
# later (build_report.json, process.log, generate_build_report.sh, …).

import os
import glob
from pathlib import Path
import textwrap
import pytest

CI_METRICS_DIR = Path("/home/user/ci_metrics").resolve()

# --------------------------------------------------------------------------- #
# Expected CSV fixture data (exact byte-for-byte, save for trailing newlines) #
# --------------------------------------------------------------------------- #
EXPECTED_CSV_CONTENTS = {
    CI_METRICS_DIR / "build_2023-05-01.csv": textwrap.dedent(
        """\
        job_id,status,duration_sec
        101,success,300
        102,failure,420
        103,success,210
        """
    ),
    CI_METRICS_DIR / "build_2023-05-02.csv": textwrap.dedent(
        """\
        job_id,status,duration_sec
        104,success,180
        105,success,240
        106,failure,360
        107,success,120
        """
    ),
    CI_METRICS_DIR / "build_2023-05-03.csv": textwrap.dedent(
        """\
        job_id,status,duration_sec
        108,failure,600
        109,failure,450
        """
    ),
}


# ------------------------------------------------------------ #
# Helper to normalise newlines when comparing text file content #
# ------------------------------------------------------------ #
def _normalise_newlines(text: str) -> str:
    """
    Convert CRLF → LF and strip exactly one trailing newline if present.
    Normalises the text so that tiny formatting differences do not break
    the test harness when they are semantically irrelevant.
    """
    text = text.replace("\r\n", "\n")
    if text.endswith("\n"):
        text = text[:-1]
    return text


# ---------------------- #
#  Test implementation   #
# ---------------------- #
def test_ci_metrics_directory_exists():
    """The /home/user/ci_metrics directory must exist and be a directory."""
    assert CI_METRICS_DIR.is_dir(), (
        f"Expected directory {CI_METRICS_DIR} to exist, "
        "but it is missing or not a directory."
    )


@pytest.mark.parametrize("csv_path,expected_content", EXPECTED_CSV_CONTENTS.items())
def test_expected_csv_files_exist_with_correct_content(csv_path: Path, expected_content: str):
    """
    Each fixture CSV file must:
      1. Exist at the exact absolute path.
      2. Contain exactly the expected bytes (ignoring the final newline).
    """
    assert csv_path.is_file(), f"Expected CSV file '{csv_path}' is missing."

    actual_content = csv_path.read_text(encoding="utf-8")
    expected_norm = _normalise_newlines(expected_content)
    actual_norm = _normalise_newlines(actual_content)

    assert actual_norm == expected_norm, (
        f"CSV file '{csv_path}' exists but its content is not what the fixture "
        "expects.\n\n--- Expected ---\n"
        f"{expected_norm}\n--- Found ---\n{actual_norm}\n"
    )


def test_no_extra_build_csv_files_present():
    """
    Aside from the three known fixture files, there must be *no* additional
    files whose names match the pattern build_*.csv.  This guards against
    accidental leakage of extra test data that could skew later calculations.
    """
    found_paths = {Path(p).resolve() for p in glob.glob(str(CI_METRICS_DIR / "build_*.csv"))}
    expected_paths = set(EXPECTED_CSV_CONTENTS.keys())

    # Provide a helpful diff if the sets don't match.
    unexpected = found_paths - expected_paths
    missing = expected_paths - found_paths

    assert not missing, (
        "The following expected CSV files are missing:\n"
        + "\n".join(f"• {p}" for p in sorted(missing))
    )
    assert not unexpected, (
        "Found unexpected CSV files matching build_*.csv that should NOT be "
        "present at the start of the exercise:\n"
        + "\n".join(f"• {p}" for p in sorted(unexpected))
    )