# test_initial_state.py
#
# This pytest suite validates the initial state of the workspace before the
# student performs any actions.  It checks only the *input* artefacts that are
# guaranteed to exist at the start of the exercise—**never** any output files
# or directories that the student is expected to create later on.

import os
import io
import pytest

# Absolute paths to the two mandatory source CSV files.
EN_CSV = "/home/user/project/translations/en_US.csv"
ES_CSV = "/home/user/project/translations/es_ES.csv"


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def _read_file_lines(path):
    """
    Read a UTF-8 file and return a list of its lines *without* any trailing
    newline characters.
    """
    with io.open(path, "r", encoding="utf-8") as fh:
        return [line.rstrip("\n") for line in fh]


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_source_files_exist():
    """
    The two source CSV files must be present and be regular files.
    """
    for path in (EN_CSV, ES_CSV):
        assert os.path.isfile(path), (
            f"Required source file is missing: {path}"
        )


def test_en_us_csv_contents():
    """
    en_US.csv must contain exactly the five expected key/value pairs and in the
    correct order.
    """
    expected = [
        "greeting,Hello",
        "farewell,Goodbye",
        "ask_name,What is your name?",
        "thank_you,Thank you",
        "welcome,Welcome",
    ]
    actual = _read_file_lines(EN_CSV)
    assert actual == expected, (
        f"Contents of {EN_CSV} are incorrect.\n"
        f"Expected lines:\n{expected}\n\nActual lines:\n{actual}"
    )


def test_es_es_csv_contents():
    """
    es_ES.csv must contain exactly the three expected key/value pairs and in the
    correct order.
    """
    expected = [
        "greeting,Hola",
        "farewell,Adiós",
        "thank_you,Gracias",
    ]
    actual = _read_file_lines(ES_CSV)
    assert actual == expected, (
        f"Contents of {ES_CSV} are incorrect.\n"
        f"Expected lines:\n{expected}\n\nActual lines:\n{actual}"
    )