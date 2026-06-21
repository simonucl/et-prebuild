# test_initial_state.py
"""
Pytest suite to validate the initial filesystem state for the
“offline mock-API” exercise.

This test file must be executed **before** the student performs any action.
It asserts that only the prerequisite directory and JSON response files
exist and that their contents are exactly as described.

If any assertion fails the error message will explicitly point out the
missing, extra or malformed element so the student immediately knows what
to fix.
"""

import json
import os
from pathlib import Path

import pytest

# ----- Constants describing the required initial state ----------------------

SAMPLES_DIR = Path("/home/user/api_samples")

EXPECTED_FILES = {
    "response1.json": {
        "id": 101,
        "status": "success",
        "elapsed_ms": 123,
        "payload": {"result": "OK"},
    },
    "response2.json": {
        "id": 102,
        "status": "error",
        "elapsed_ms": 456,
        "payload": {"result": "FAIL"},
    },
}

# The exact, canonical textual representation (no extra spaces or commas)
EXPECTED_TEXTS = {
    "response1.json": (
        '{\n'
        '  "id": 101,\n'
        '  "status": "success",\n'
        '  "elapsed_ms": 123,\n'
        '  "payload": {\n'
        '    "result": "OK"\n'
        '  }\n'
        '}\n'
    ),
    "response2.json": (
        '{\n'
        '  "id": 102,\n'
        '  "status": "error",\n'
        '  "elapsed_ms": 456,\n'
        '  "payload": {\n'
        '    "result": "FAIL"\n'
        '  }\n'
        '}\n'
    ),
}


# ---------------------------------------------------------------------------


def test_samples_directory_exists_and_is_dir():
    """
    /home/user/api_samples must exist and be a directory.
    """
    assert SAMPLES_DIR.exists(), (
        f"Required directory {SAMPLES_DIR} is missing."
    )
    assert SAMPLES_DIR.is_dir(), (
        f"{SAMPLES_DIR} exists but is not a directory."
    )


def test_samples_directory_permissions():
    """
    Directory must be readable & executable by the owner.
    (Exact mode 755 is not enforced – only that owner can read and execute.)
    """
    mode = SAMPLES_DIR.stat().st_mode
    # Owner-read (0o400) and owner-exec (0o100) bits must be set.
    assert mode & 0o500 == 0o500, (
        f"{SAMPLES_DIR} should have at least r-x permissions for the owner."
    )


def test_directory_contains_exactly_two_json_files():
    """
    The directory must contain *only* response1.json and response2.json.
    No other files or sub-directories are permitted at this stage.
    """
    entries = [entry.name for entry in SAMPLES_DIR.iterdir()]
    # Filter out the expected files
    extras = sorted(set(entries) - EXPECTED_FILES.keys())
    missing = sorted(set(EXPECTED_FILES.keys()) - set(entries))

    assert not missing, (
        f"Missing required file(s) in {SAMPLES_DIR}: {', '.join(missing)}"
    )
    assert not extras, (
        f"Unexpected file(s) present in {SAMPLES_DIR}: {', '.join(extras)}"
    )


@pytest.mark.parametrize("filename, expected_obj", EXPECTED_FILES.items())
def test_json_file_contents_are_exact(filename, expected_obj):
    """
    Each JSON file must:
      1. Be valid JSON.
      2. Contain exactly the expected object (no extra keys/values).
      3. Have no superfluous characters (whitespace other than the canonical
         indentation is disallowed).
    """
    file_path = SAMPLES_DIR / filename
    text = file_path.read_text(encoding="utf-8")

    # 1. Parse JSON
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as exc:
        pytest.fail(f"{filename} is not valid JSON: {exc}")

    # 2. Object equality check
    assert parsed == expected_obj, (
        f"{filename} does not contain the expected JSON object.\n"
        f"Expected: {expected_obj}\nFound   : {parsed}"
    )

    # 3. Exact textual match (ensures no extra spaces, commas or lines)
    #    We compare against the canonical representation provided above.
    canonical_text = EXPECTED_TEXTS[filename]
    assert text == canonical_text, (
        f"{filename} has unexpected formatting or whitespace."
    )


def test_summary_and_log_files_are_absent_initially():
    """
    summary.csv and process.log must NOT exist before the student runs
    their solution script. (They will be created later.)
    This test is informational: it fails only if those files already exist,
    which would indicate that the starting environment is polluted.
    """
    for fname in ("summary.csv", "process.log"):
        fpath = SAMPLES_DIR / fname
        assert not fpath.exists(), (
            f"Output file {fpath} should not exist before the task begins."
        )