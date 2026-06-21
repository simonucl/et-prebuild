# test_initial_state.py
#
# This pytest suite verifies the *initial* filesystem state before
# the student runs any commands.  It intentionally asserts only the
# presence and exact content of the staged “API” source artifacts.
#
# Do NOT add tests for the files/directories that the student is
# expected to create later (/home/user/prep/*).

import os
import pytest

API_DIR = "/home/user/api_source"
SCHEMA_PATH = os.path.join(API_DIR, "dataset_schema.json")

# The exact JSON payload that must already be available.
EXPECTED_SCHEMA = (
    '{\n'
    '  "dataset": "iris",\n'
    '  "version": "1.0",\n'
    '  "features": ["sepal_length", "sepal_width", "petal_length", "petal_width"],\n'
    '  "target": "species",\n'
    '  "classes": ["setosa", "versicolor", "virginica"]\n'
    '}\n'
)


def test_api_source_directory_exists():
    """Ensure the mock API directory is present before the learner starts."""
    assert os.path.isdir(API_DIR), (
        f"Required directory {API_DIR!r} is missing. "
        "The mock API source must be in place before the task begins."
    )


def test_dataset_schema_file_exists():
    """Ensure the dataset_schema.json file exists inside the API directory."""
    assert os.path.isfile(SCHEMA_PATH), (
        f"Required file {SCHEMA_PATH!r} is missing. "
        "The learner cannot fetch the payload if it is absent."
    )


def test_dataset_schema_content_exact_match():
    """Ensure that dataset_schema.json matches the expected byte‐for‐byte content."""
    with open(SCHEMA_PATH, "r", encoding="utf-8") as fp:
        actual = fp.read()
    assert actual == EXPECTED_SCHEMA, (
        "The content of dataset_schema.json does not match the expected payload.\n\n"
        "If this file was modified, restore it to the exact JSON shown in the "
        "task description so that the learner can copy it byte-for-byte."
    )