# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state **before** the
# student starts working.  Only the unsorted French JSON file must be present.
# No derivative artefacts (sorted JSON/CSV or log files) are allowed yet.

import json
from pathlib import Path

import pytest

I18N_DIR = Path("/home/user/project/i18n")
FR_JSON = I18N_DIR / "fr.json"
FR_SORTED_JSON = I18N_DIR / "fr_sorted.json"
FR_SORTED_CSV = I18N_DIR / "fr_sorted.csv"
PROCESS_LOG = I18N_DIR / "process.log"

# The exact, expected contents of the initial fr.json (including trailing \n)
EXPECTED_FR_JSON_CONTENT = """{
  "CancelButton": "Annuler",
  "AddButton": "Ajouter",
  "DeleteDialogTitle": "Supprimer l’élément ?",
  "EditLabel": "Modifier",
  "SaveSuccess": "Enregistré avec succès"
}
"""


def test_i18n_directory_exists():
    assert I18N_DIR.is_dir(), (
        f"The directory {I18N_DIR} should exist before starting the task."
    )


def test_only_fr_json_exists_initially():
    """
    Exactly one deliverable file must be present at the outset: fr.json.
    Derivative artefacts must **not** exist yet.
    """
    assert FR_JSON.is_file(), f"Required file {FR_JSON} is missing."

    for path in (FR_SORTED_JSON, FR_SORTED_CSV, PROCESS_LOG):
        assert not path.exists(), (
            f"The file {path} must NOT exist before the task begins."
        )


def test_fr_json_content_exact_match():
    """
    The fr.json file must have the precise, unsorted content provided by the
    localization engineer (byte-for-byte, including the final newline).
    """
    content = FR_JSON.read_text(encoding="utf-8")
    assert content == EXPECTED_FR_JSON_CONTENT, (
        "The content of fr.json does not match the expected initial state. "
        "It must remain unmodified until the task is completed."
    )


def test_fr_json_parses_and_has_five_keys():
    """
    Sanity-check: the JSON parses correctly and contains exactly 5 key/value
    pairs.  (Parsing also ensures the test above used valid JSON text.)
    """
    data = json.loads(EXPECTED_FR_JSON_CONTENT)
    assert isinstance(data, dict), "fr.json should contain a JSON object."
    assert len(data) == 5, "fr.json must contain exactly 5 translation keys."


def test_initial_key_order_is_unsorted():
    """
    Confirm that the keys are *not* in lexicographical order yet, ensuring that
    the student really needs to perform a sorting operation.
    """
    keys = list(json.loads(EXPECTED_FR_JSON_CONTENT).keys())
    assert keys != sorted(keys), (
        "The keys in fr.json appear to be already sorted; they should be "
        "unsorted in the initial state."
    )