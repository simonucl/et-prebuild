# test_initial_state.py
#
# This pytest file validates that the *initial* state of the operating
# system / filesystem is exactly as expected **before** the student
# starts working on the assignment.
#
# It checks:
#   • Presence and exact content of /home/user/projects/l10n/en_US.csv
#   • Presence and exact content of /home/user/projects/l10n/fr_FR.json
#   • Absence of /home/user/projects/l10n/update.log
#   • No stray files inside /home/user/projects/l10n/
#
# Only the Python standard library and pytest are used.

import json
import os
from pathlib import Path

import pytest

L10N_DIR = Path("/home/user/projects/l10n")
EN_CSV = L10N_DIR / "en_US.csv"
FR_JSON = L10N_DIR / "fr_FR.json"
UPDATE_LOG = L10N_DIR / "update.log"

EXPECTED_CSV = (
    "key,text\n"
    "app.title,Weather App\n"
    "app.greeting,Hello!\n"
    "error.network,Network error\n"
    "menu.settings,Settings\n"
    "menu.quit,Quit\n"
)

EXPECTED_JSON = (
    "{\n"
    '  "app.title": "Application Météo",\n'
    '  "menu.settings": "Paramètres"\n'
    "}\n"
)

EXPECTED_FILES = {EN_CSV.name, FR_JSON.name}  # update.log must NOT exist yet


def _read_text(path: Path) -> str:
    """Helper that always reads file as UTF-8 text."""
    with path.open("r", encoding="utf-8", newline="") as fp:
        return fp.read()


def test_l10n_directory_exists():
    assert L10N_DIR.is_dir(), (
        f"Expected directory {L10N_DIR} to exist but it does not."
    )


def test_only_expected_files_present():
    files_present = {p.name for p in L10N_DIR.iterdir() if p.is_file()}
    assert files_present == EXPECTED_FILES, (
        f"{L10N_DIR} should initially contain exactly the files "
        f"{sorted(EXPECTED_FILES)}, but it currently contains "
        f"{sorted(files_present)}."
    )


def test_en_us_csv_content_exact():
    assert EN_CSV.is_file(), f"Missing file: {EN_CSV}"
    text = _read_text(EN_CSV)
    assert text == EXPECTED_CSV, (
        f"Content of {EN_CSV} differs from expected initial state.\n"
        "---- expected ------------------------------------------------\n"
        f"{EXPECTED_CSV}"
        "---- found ---------------------------------------------------\n"
        f"{text}"
        "--------------------------------------------------------------"
    )
    assert text.endswith("\n"), f"{EN_CSV} must end with a single trailing newline."


def test_fr_fr_json_content_exact():
    assert FR_JSON.is_file(), f"Missing file: {FR_JSON}"
    text = _read_text(FR_JSON)
    assert text == EXPECTED_JSON, (
        f"Content of {FR_JSON} differs from expected initial state.\n"
        "---- expected ------------------------------------------------\n"
        f"{EXPECTED_JSON}"
        "---- found ---------------------------------------------------\n"
        f"{text}"
        "--------------------------------------------------------------"
    )
    assert text.endswith("\n"), f"{FR_JSON} must end with a single trailing newline."

    # Additional validation: make sure it's valid JSON and contains the two keys
    data = json.loads(text)
    assert set(data) == {"app.title", "menu.settings"}, (
        f"{FR_JSON} should only contain keys "
        f"{{'app.title', 'menu.settings'}} but found {set(data)}."
    )


def test_update_log_absent():
    assert not UPDATE_LOG.exists(), (
        f"{UPDATE_LOG} should NOT exist before the student runs their solution."
    )