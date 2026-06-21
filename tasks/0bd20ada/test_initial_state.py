# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem state
# before the student performs any actions.

import os
import stat
from pathlib import Path

DATASET_DIR = Path("/home/user/datasets")
GENES_TSV = DATASET_DIR / "genes.tsv"
EXPR_TSV = DATASET_DIR / "expression.tsv"
SAMPLE_INFO_TSV = DATASET_DIR / "sample_info.tsv"

SUMMARY_AB = DATASET_DIR / "summary_ab.tsv"
SUMMARY_C = DATASET_DIR / "summary_c.tsv"

RESEARCH_LOG_DIR = Path("/home/user/research_logs")
RESEARCH_LOG_FILE = RESEARCH_LOG_DIR / "column_extraction.log"


# ---------------------------------------------------------------------------#
# Helper expectations                                                         #
# ---------------------------------------------------------------------------#
EXPECTED_GENES = (
    "gene_id\tgene_name\tchromosome\n"
    "1\tTP53\t17\n"
    "2\tEGFR\t7\n"
    "3\tBRCA1\t17\n"
    "4\tMYC\t8\n"
    "5\tMTOR\t1\n"
)

EXPECTED_EXPRESSION = (
    "gene_id\tsample_A\tsample_B\tsample_C\n"
    "1\t12.5\t13.0\t11.8\n"
    "2\t4.2\t4.9\t5.0\n"
    "3\t7.7\t8.1\t7.5\n"
    "4\t20.0\t19.5\t21.1\n"
    "5\t10.3\t9.8\t10.0\n"
)

EXPECTED_SAMPLE_INFO = (
    "sample_id\ttissue\tcondition\n"
    "sample_A\tliver\ttreated\n"
    "sample_B\tliver\tcontrol\n"
    "sample_C\theart\ttreated\n"
)


# ---------------------------------------------------------------------------#
# Tests                                                                       #
# ---------------------------------------------------------------------------#
def _assert_mode_0644(path: Path) -> None:
    """Helper that asserts rw-r--r-- (0644) permissions on a file."""
    mode = stat.S_IMODE(path.stat().st_mode)
    assert mode == 0o644, f"File {path} should have permissions 0644; found {oct(mode)}"


def test_dataset_directory_exists():
    assert DATASET_DIR.is_dir(), f"Expected directory {DATASET_DIR} to exist."


def test_genes_tsv_contents_and_mode():
    assert GENES_TSV.is_file(), f"Missing file: {GENES_TSV}"
    content = GENES_TSV.read_text(encoding="utf-8")
    assert content == EXPECTED_GENES, (
        f"Contents of {GENES_TSV} do not match expected initial state."
    )
    _assert_mode_0644(GENES_TSV)


def test_expression_tsv_contents_and_mode():
    assert EXPR_TSV.is_file(), f"Missing file: {EXPR_TSV}"
    content = EXPR_TSV.read_text(encoding="utf-8")
    assert content == EXPECTED_EXPRESSION, (
        f"Contents of {EXPR_TSV} do not match expected initial state."
    )
    _assert_mode_0644(EXPR_TSV)


def test_sample_info_tsv_contents_and_mode():
    assert SAMPLE_INFO_TSV.is_file(), f"Missing file: {SAMPLE_INFO_TSV}"
    content = SAMPLE_INFO_TSV.read_text(encoding="utf-8")
    assert content == EXPECTED_SAMPLE_INFO, (
        f"Contents of {SAMPLE_INFO_TSV} do not match expected initial state."
    )
    _assert_mode_0644(SAMPLE_INFO_TSV)


def test_summary_files_do_not_exist_yet():
    assert not SUMMARY_AB.exists(), (
        f"{SUMMARY_AB} should NOT exist before the exercise is completed."
    )
    assert not SUMMARY_C.exists(), (
        f"{SUMMARY_C} should NOT exist before the exercise is completed."
    )


def test_research_log_directory_and_file_absent():
    # The directory itself may or may not exist; if it exists,
    # it must not yet contain the log file.
    if RESEARCH_LOG_DIR.exists():
        assert RESEARCH_LOG_DIR.is_dir(), (
            f"{RESEARCH_LOG_DIR} exists but is not a directory."
        )
        assert not RESEARCH_LOG_FILE.exists(), (
            f"{RESEARCH_LOG_FILE} should not exist before any commands are run."
        )
    else:
        # Directory entirely absent is also acceptable for initial state
        assert not RESEARCH_LOG_FILE.exists(), (
            f"{RESEARCH_LOG_FILE} should not exist before any commands are run."
        )