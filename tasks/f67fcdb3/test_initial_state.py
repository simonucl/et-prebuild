# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state **before** the
# student performs any action.  It checks that the expected CSV file exists
# and contains exactly the contents described in the task—most importantly
# that the French (“fr”) column for the key “WELCOME” is still empty.
#
# NOTE:  Per the authoring rules, we intentionally do *not* test for the
#        presence or absence of any output artefacts such as `fr.json`.

import pathlib
import csv
import pytest

# Constants
CSV_PATH = pathlib.Path("/home/user/project/localization/translations.csv")

EXPECTED_ROWS = [
    ["key", "en", "fr", "de"],
    ["WELCOME", "Welcome", "", "Willkommen"],
    ["EXIT", "Exit", "Quitter", "Beenden"],
    ["SAVE", "Save", "Enregistrer", "Speichern"],
    ["CANCEL", "Cancel", "Annuler", "Abbrechen"],
    ["DELETE", "Delete", "Supprimer", "Löschen"],
]

@pytest.fixture(scope="module")
def csv_lines():
    """Read the CSV as raw lines (without trailing newline ambiguity)."""
    if not CSV_PATH.exists():
        pytest.fail(f"Expected CSV file not found at {CSV_PATH}")
    if not CSV_PATH.is_file():
        pytest.fail(f"Expected {CSV_PATH} to be a regular file")

    # Read the file in text mode using UTF-8; splitlines() drops trailing \n.
    raw_text = CSV_PATH.read_text(encoding="utf-8")
    return raw_text.splitlines()


def test_line_count(csv_lines):
    """The CSV must contain exactly 6 lines (1 header + 5 data rows)."""
    assert len(csv_lines) == 6, (
        f"{CSV_PATH} should have exactly 6 lines "
        f"(1 header + 5 rows), found {len(csv_lines)}."
    )


def test_exact_contents(csv_lines):
    """
    Verify that every line matches the expected value, including the
    still-missing French translation for the key 'WELCOME'.
    """
    # Compare line-by-line content.
    for idx, (actual, expected) in enumerate(zip(csv_lines, map(lambda r: ",".join(r), EXPECTED_ROWS))):
        assert actual == expected, (
            f"Line {idx + 1} in {CSV_PATH} is incorrect.\n"
            f"Expected: {expected!r}\n"
            f"Found:    {actual!r}"
        )


def test_csv_parsing(csv_lines):
    """
    Additionally parse the CSV to make sure the column structure is correct
    and that the 'fr' entry for 'WELCOME' is truly empty.
    """
    reader = csv.DictReader(csv_lines)
    rows = {row["key"]: row for row in reader}

    # Basic structural assertions
    expected_keys = {"WELCOME", "EXIT", "SAVE", "CANCEL", "DELETE"}
    assert set(rows) == expected_keys, (
        f"CSV keys mismatch.\nExpected: {sorted(expected_keys)}\n"
        f"Found:    {sorted(rows)}"
    )

    # Specific check: WELCOME has empty French translation
    welcome_fr = rows["WELCOME"]["fr"]
    assert welcome_fr == "", (
        "The French translation for 'WELCOME' should be empty in the "
        "initial state, but it is currently set to "
        f"{welcome_fr!r}."
    )