# test_initial_state.py
"""
Pytest suite that verifies the ORIGINAL, vulnerable ETL proof-of-concept
is exactly as expected *before* the learner starts the remediation work.

The checks purposely validate only the files that must already exist.
Nothing about the future “fixed” artefacts (e.g., test_input.json,
security_fix.log) is asserted here, in order to stay compliant with
the grading rules.
"""

import importlib
import os
import sys
from pathlib import Path

import pytest

# ---------- Fixed, absolute project paths ----------
ETL_DIR = Path("/home/user/etl")
TRANSFORM_PY = ETL_DIR / "transform.py"
EXTRACT_PY = ETL_DIR / "extract.py"
LOAD_PY = ETL_DIR / "load.py"
SAMPLE_PKL = ETL_DIR / "sample.pkl"
README_MD = ETL_DIR / "README.md"
REQ_TXT = ETL_DIR / "requirements.txt"


# ---------- Helper to import the current, vulnerable transform.py ----------
def _import_transform_module():
    """
    Dynamically import /home/user/etl/transform.py without relying on the
    environment’s PYTHONPATH.  This lets us call transform.transform(...)
    exactly as the initial proof-of-concept would.
    """
    sys.path.insert(0, str(ETL_DIR))
    try:
        return importlib.import_module("transform")
    finally:
        # Clean up to avoid polluting global import state for other tests
        if sys.path[0] == str(ETL_DIR):
            sys.path.pop(0)


# ---------- Tests ----------

def test_project_files_exist():
    """
    The starter repository must contain every file advertised in the
    task description.
    """
    missing = [
        p for p in
        (TRANSFORM_PY, EXTRACT_PY, LOAD_PY, SAMPLE_PKL, README_MD, REQ_TXT)
        if not p.exists()
    ]
    assert not missing, (
        "The following expected starter file(s) are missing:\n" +
        "\n".join(str(p) for p in missing)
    )


def test_requirements_is_empty():
    """
    requirements.txt should be completely empty at the outset.
    Leading/trailing whitespace is tolerated, but there must be no
    package names.
    """
    content = REQ_TXT.read_text(encoding="utf-8").strip()
    assert content == "", (
        "/home/user/etl/requirements.txt must be empty in the initial "
        "state, but contains:\n"
        f"{content}"
    )


def test_transform_contains_pickle_and_no_json():
    """
    The vulnerable proof-of-concept must clearly use the unsafe
    `pickle` module, and should NOT yet reference `json` for
    deserialisation.
    """
    source = TRANSFORM_PY.read_text(encoding="utf-8")
    assert "import pickle" in source, (
        "transform.py should import the *unsafe* 'pickle' module "
        "in the initial state, but the import is missing."
    )
    assert "pickle.load" in source, (
        "transform.py should use pickle.load(...) in the initial state."
    )
    assert "json" not in source, (
        "transform.py unexpectedly references 'json' in the initial "
        "state. It should still be vulnerable at this point."
    )


def test_sample_pkl_can_be_deserialised_by_transform():
    """
    Calling the transform() function on sample.pkl must succeed and
    produce the expected Python object: {'fresh': True, 'rows': 17}.
    This confirms both the file’s presence and the behaviour of the
    vulnerable code.
    """
    transform_mod = _import_transform_module()
    expected = {"fresh": True, "rows": 17}
    actual = transform_mod.transform(str(SAMPLE_PKL))
    assert actual == expected, (
        f"transform.transform('{SAMPLE_PKL}') returned {actual!r}, "
        f"but the expected object is {expected!r}."
    )