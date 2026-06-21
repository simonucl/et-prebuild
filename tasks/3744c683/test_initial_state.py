# test_initial_state.py
#
# Pytest suite that validates the initial filesystem state expected by the
# “Research Datasets” exercise _before_ the student performs any actions.
#
# The checks assert that:
#   • The three dataset directories exist under /home/user/research_datasets.
#   • Each dataset contains the correct meta.json file with the exact expected
#     content (description, rows, columns).
#   • The companion data file for each dataset exists.
#   • No /home/user/research_datasets/docs directory (or its deliverables)
#     exists yet, because the student is expected to create them.
#
# If any assertion fails, the error message explains precisely what is
# missing or incorrect so the student can immediately see what to fix.

import json
import os
from pathlib import Path

import pytest

BASE_DIR = Path("/home/user/research_datasets")

# Ground-truth description of the expected workspace -------------------------------------------
DATASETS = {
    "climate_data": {
        "description": "Daily world surface temperature readings.",
        "rows": 36500,
        "columns": 8,
        "extra_files": ["data.csv"],
    },
    "ocean_salinity": {
        "description": "Global ocean surface salinity measurements.",
        "rows": 54000,
        "columns": 6,
        "extra_files": ["salinity.csv"],
    },
    "star_catalog": {
        "description": "Stellar positions and magnitudes from deep-sky survey.",
        "rows": 112000,
        "columns": 12,
        "extra_files": ["stars.parquet"],
    },
}


# Helper ----------------------------------------------------------------------
def read_json(path: Path):
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


# Tests -----------------------------------------------------------------------
def test_base_directory_exists_and_is_directory():
    assert BASE_DIR.exists(), f"Expected base directory {BASE_DIR} to exist."
    assert BASE_DIR.is_dir(), f"{BASE_DIR} exists but is not a directory."


@pytest.mark.parametrize("dataset_name", sorted(DATASETS.keys()))
def test_dataset_directory_structure_and_files(dataset_name):
    meta = DATASETS[dataset_name]
    ds_dir = BASE_DIR / dataset_name

    # 1. Directory presence ----------------------------------------------------
    assert ds_dir.exists(), f"Dataset directory {ds_dir} is missing."
    assert ds_dir.is_dir(), f"{ds_dir} exists but is not a directory."

    # 2. Extra data files ------------------------------------------------------
    for fname in meta["extra_files"]:
        data_file = ds_dir / fname
        assert data_file.exists(), f"Expected data file {data_file} is missing."
        assert data_file.is_file(), f"{data_file} exists but is not a regular file."

    # 3. meta.json presence ----------------------------------------------------
    meta_path = ds_dir / "meta.json"
    assert meta_path.exists(), f"{meta_path} is missing."
    assert meta_path.is_file(), f"{meta_path} exists but is not a regular file."

    # 4. meta.json content -----------------------------------------------------
    parsed = read_json(meta_path)

    for key in ("description", "rows", "columns"):
        assert key in parsed, f"{meta_path}: key '{key}' is missing."

    assert parsed["description"] == meta["description"], (
        f"{meta_path}: description mismatch.\n"
        f"  Expected: {meta['description']!r}\n"
        f"  Found:    {parsed['description']!r}"
    )
    assert parsed["rows"] == meta["rows"], (
        f"{meta_path}: rows mismatch (expected {meta['rows']}, got {parsed['rows']})."
    )
    assert parsed["columns"] == meta["columns"], (
        f"{meta_path}: columns mismatch (expected {meta['columns']}, got {parsed['columns']})."
    )


def test_no_docs_directory_yet():
    """
    The student must create /home/user/research_datasets/docs/ later, so at the
    initial state it should NOT exist.
    """
    docs_dir = BASE_DIR / "docs"
    assert not docs_dir.exists(), (
        f"Directory {docs_dir} already exists, "
        "but it should be created by the student during the exercise."
    )


def test_no_deliverables_exist_yet():
    """
    README.md and lint_report.log must not pre-exist.  Their presence now would
    indicate that the initial workspace has been modified already.
    """
    readme = BASE_DIR / "docs" / "README.md"
    lint_log = BASE_DIR / "docs" / "lint_report.log"

    assert not readme.exists(), f"Unexpected file already present: {readme}"
    assert not lint_log.exists(), f"Unexpected file already present: {lint_log}"