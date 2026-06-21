# test_initial_state.py
#
# Pytest suite to validate the starting state of the localisation project
# BEFORE the student makes any changes.
#
# Rules enforced:
#   • Presence of the expected files/directories
#   • Exact contents of the .env file (3 lines, trailing newline, no blanks)
#   • Spanish & English JSON catalogues exist, are single-line, valid JSON,
#     and contain only the predefined key/value pairs
#
# NOTE:  This file intentionally does NOT test for update_log.txt (the
#        "output" artefact).  We only check the initial, pre-task state.

import json
from pathlib import Path

PROJECT_ROOT = Path("/home/user/project-l18n")
ENV_FILE = PROJECT_ROOT / ".env"
EN_JSON = PROJECT_ROOT / "translations" / "messages.en.json"
ES_JSON = PROJECT_ROOT / "translations" / "messages.es.json"


def test_project_structure():
    assert PROJECT_ROOT.is_dir(), (
        f"Expected project directory '{PROJECT_ROOT}' to exist."
    )
    assert ENV_FILE.is_file(), (
        f"Missing env file: '{ENV_FILE}'."
    )
    assert EN_JSON.is_file(), (
        f"Missing English catalogue: '{EN_JSON}'."
    )
    assert ES_JSON.is_file(), (
        f"Missing Spanish catalogue: '{ES_JSON}'."
    )


def test_env_file_contents():
    raw = ENV_FILE.read_bytes()
    text = raw.decode("utf-8")

    # 1. File must end with exactly one trailing newline
    assert text.endswith("\n"), (
        ".env file must end with a single trailing newline."
    )
    assert not text.endswith("\n\n"), (
        ".env file contains extra blank line(s) at the end."
    )

    # 2. Split lines and verify exact count & ordering
    lines = text.splitlines()  # removes the trailing newline
    expected_lines = [
        "API_URL=https://api.example.com",
        "FEATURE_X=true",
        "MAX_RETRIES=5",
    ]
    assert lines == expected_lines, (
        "Contents of .env are incorrect.\n"
        f"Expected lines:\n{expected_lines}\n\nActual lines:\n{lines}"
    )

    # 3. Ensure no line has trailing spaces
    for idx, line in enumerate(text.split("\n")[:-1], start=1):  # ignore final ''
        assert not line.rstrip("\n").endswith(" "), (
            f"Line {idx} in .env ends with a space, which is not allowed:\n{repr(line)}"
        )

    # 4. Exactly three newline characters (one per expected line)
    newline_count = text.count("\n")
    assert newline_count == 3, (
        f".env should contain 3 newline characters (one per line); found {newline_count}."
    )


def _load_single_line_json(path: Path, expected_dict: dict):
    """
    Helper: ensure the file is single-line, ends with '\n',
    parses as JSON, and matches the expected mapping.
    """
    raw = path.read_bytes()
    txt = raw.decode("utf-8")

    # File must be single-line with exactly one trailing newline character
    assert txt.endswith("\n"), f"{path} must end with a trailing newline."
    assert txt.count("\n") == 1, f"{path} must be a single-line JSON object."
    json_str = txt.rstrip("\n")  # strip trailing newline for JSON parsing

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as exc:
        raise AssertionError(f"{path} contains invalid JSON: {exc}") from exc

    assert data == expected_dict, (
        f"Unexpected contents in {path}.\n"
        f"Expected: {expected_dict}\nActual:   {data}"
    )


def test_english_catalogue():
    expected = {"hello": "Hello", "bye": "Good-bye"}
    _load_single_line_json(EN_JSON, expected)


def test_spanish_catalogue():
    expected = {"hello": "Hola", "bye": "Adiós"}
    _load_single_line_json(ES_JSON, expected)