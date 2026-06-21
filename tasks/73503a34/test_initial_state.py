# test_initial_state.py
# Pytest suite that verifies the expected *initial* filesystem state
# before the student runs any commands.

import json
import os
from pathlib import Path

# Constants ------------------------------------------------------------------

HOME = Path("/home/user")
DATA_DIR = HOME / "data"
OUTPUT_DIR = HOME / "output"

TRAINING_JSON = DATA_DIR / "training_samples.json"
SCHEMA_JSON = DATA_DIR / "feature_schema.json"

VALID_SAMPLES_JSON = OUTPUT_DIR / "valid_samples.json"
VALIDATION_LOG = OUTPUT_DIR / "validation.log"

# ---------------------------------------------------------------------------

EXPECTED_TRAINING_CONTENT = [
    {"id": "001", "features": [0.1, 0.5, 0.2], "label": "positive"},
    {"id": "002", "features": [0.3, 0.6], "label": "negative"},
    {"id": "003", "features": [0.4, 0.2, 0.1], "label": "neutral"},
    {"id": "004", "features": [0.8, 0.9, 0.7], "label": "negative"},
    {"id": "005", "id_extra": "something", "features": [0.2, 0.4, 0.5], "label": "positive"},
]

EXPECTED_SCHEMA_CONTENT = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["id", "features", "label"],
    "properties": {
        "id": {"type": "string"},
        "features": {
            "type": "array",
            "items": {"type": "number"},
            "minItems": 3,
            "maxItems": 3,
        },
        "label": {"type": "string", "enum": ["positive", "negative"]},
    },
    "additionalProperties": True,
}


# Helper ---------------------------------------------------------------------

def load_json(path: Path):
    """Load and return JSON from a file."""
    with path.open() as fh:
        return json.load(fh)


# Tests ----------------------------------------------------------------------

def test_directories_exist():
    """Required directories must already exist."""
    assert DATA_DIR.is_dir(), f"Missing directory: {DATA_DIR}"
    assert OUTPUT_DIR.is_dir(), f"Missing directory: {OUTPUT_DIR}"


def test_training_samples_file_content():
    """training_samples.json must exist and contain the expected data."""
    assert TRAINING_JSON.is_file(), f"Missing file: {TRAINING_JSON}"
    actual = load_json(TRAINING_JSON)

    # Basic shape checks
    assert isinstance(actual, list), "training_samples.json must be a JSON array."
    assert len(actual) == 5, "training_samples.json must contain exactly 5 objects."

    # Exact content check
    assert actual == EXPECTED_TRAINING_CONTENT, (
        "training_samples.json content does not match the expected initial data."
    )


def test_feature_schema_content():
    """feature_schema.json must exist and contain the documented schema."""
    assert SCHEMA_JSON.is_file(), f"Missing file: {SCHEMA_JSON}"
    actual = load_json(SCHEMA_JSON)

    # Since JSON order isn't guaranteed, compare dicts directly.
    assert actual == EXPECTED_SCHEMA_CONTENT, (
        "feature_schema.json content differs from the expected informal schema."
    )


def test_output_directory_initially_empty():
    """
    The output directory must exist but *not* yet contain the artefacts
    that the student is supposed to create.
    """
    # We do NOT require the directory to be completely empty—only that the two
    # specific files have not been created yet.
    assert not VALID_SAMPLES_JSON.exists(), (
        f"{VALID_SAMPLES_JSON} should NOT exist before the task is performed."
    )
    assert not VALIDATION_LOG.exists(), (
        f"{VALIDATION_LOG} should NOT exist before the task is performed."
    )