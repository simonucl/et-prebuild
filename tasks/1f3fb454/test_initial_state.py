# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state **before** the
# student executes any commands.  It checks that the original CSV is present
# and unmodified, and that the two artefacts the student is supposed to
# create do **not** yet exist.

import os
import pytest

BASE_DIR = "/home/user/project/translations"
MSG_CSV = os.path.join(BASE_DIR, "messages.csv")
UPDATED_CSV = os.path.join(BASE_DIR, "updated_messages.csv")
LOG_FILE = os.path.join(BASE_DIR, "update_log.txt")


# --------------------------------------------------------------------------- #
# Expected content of the pre-existing CSV (11 lines, each ending with LF)
# --------------------------------------------------------------------------- #
EXPECTED_LINES = [
    "key,en,de,fr,es,it",
    "greeting,Hello,Hallo,Bonjour,Hola,Ciao",
    "farewell,Goodbye,Auf Wiedersehen,Au revoir,Adiós,Arrivederci",
    "thank_you,Thank you,Danke,Merci,Gracias,Grazie",
    "yes,Yes,Ja,Oui,Sí,Sì",
    "no,No,Nein,Non,No,Nessuno",
    "please,Please,Bitte,S'il vous plaît,Por favor,Per favore",
    "sorry,Sorry,Entschuldigung,Désolé,Lo siento,Mi dispiace",
    "welcome,Welcome,Willkommen,Bienvenue,Bienvenido,Benvenuto",
    "congrats,Congratulations,Herzlichen Glückwunsch,Félicitations,Felicitaciones,Congratulazioni",
    "morning,Good morning,Guten Morgen,Bonjour,Buenos días,Buongiorno",
]
EXPECTED_CONTENT = "\n".join(EXPECTED_LINES) + "\n"  # Each line must end with LF


# --------------------------------------------------------------------------- #
# Tests for the initial state
# --------------------------------------------------------------------------- #
def test_messages_csv_exists():
    """The original CSV must exist."""
    assert os.path.isfile(MSG_CSV), (
        f"Required file not found: {MSG_CSV}\n"
        "Make sure the initial dataset is present at the correct path."
    )


def test_messages_csv_content():
    """The original CSV must be byte-for-byte identical to the expected content."""
    with open(MSG_CSV, "rb") as fp:
        actual_bytes = fp.read()
    try:
        actual_text = actual_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        pytest.fail(f"{MSG_CSV} is not valid UTF-8: {exc}")

    assert actual_text == EXPECTED_CONTENT, (
        f"{MSG_CSV} does not match the expected initial content.\n"
        "Differences detected between the on-disk file and the canonical data."
    )

    # Additional sanity checks (helpful error messages if formatting is off)
    lines = actual_text.splitlines(keepends=True)
    assert len(lines) == 11, (
        f"{MSG_CSV} should contain exactly 11 lines (1 header + 10 data rows); "
        f"found {len(lines)}."
    )
    for idx, line in enumerate(lines, 1):
        assert line.endswith("\n"), (
            f"Line {idx} of {MSG_CSV} is missing the required trailing LF."
        )


def test_no_updated_files_yet():
    """
    The files that the student is expected to create must *not* exist
    before any action has been taken.
    """
    assert not os.path.exists(UPDATED_CSV), (
        f"{UPDATED_CSV} should NOT exist yet. "
        "Delete it before running your solution."
    )
    assert not os.path.exists(LOG_FILE), (
        f"{LOG_FILE} should NOT exist yet. "
        "Delete it before running your solution."
    )