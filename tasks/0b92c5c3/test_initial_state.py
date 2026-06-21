# test_initial_state.py
#
# This pytest suite checks the **initial** state of the operating system
# before the student performs any actions.  It asserts that
#
# • /home/user/profiling/raw_logs exists
# • It contains exactly three UTF-8 log files: run1.log, run2.log, run3.log
# • The contents of those files exactly match the pre-seeded data
# • Every line in every log file is a valid JSON object whose keys appear
#   in the required order (timestamp, cpu, mem)
#
# No checks are performed for the output artefacts that the student will
# create later (summary CSV, tarball, etc.) in accordance with the rules.

import json
import os
import pathlib
import re

import pytest

RAW_DIR = pathlib.Path("/home/user/profiling/raw_logs")

# ---------------------------------------------------------------------------
# 1. Directory & file presence
# ---------------------------------------------------------------------------


def test_raw_logs_directory_exists_and_contains_expected_files():
    """The seed directory and the three log files must be present—nothing else."""
    assert RAW_DIR.is_dir(), f"Required directory {RAW_DIR} is missing."

    present_files = sorted(f.name for f in RAW_DIR.iterdir() if f.is_file())
    expected_files = ["run1.log", "run2.log", "run3.log"]

    assert (
        present_files == expected_files
    ), f"{RAW_DIR} must contain exactly {expected_files}. Found: {present_files}"


# ---------------------------------------------------------------------------
# 2. Exact file contents (byte-for-byte)
# ---------------------------------------------------------------------------

EXPECTED_CONTENTS = {
    "run1.log": (
        '{"timestamp":"2023-06-01T10:00:00Z","cpu":10.5,"mem":104857}\n'
        '{"timestamp":"2023-06-01T10:00:05Z","cpu":25.0,"mem":209715}\n'
        '{"timestamp":"2023-06-01T10:00:10Z","cpu":30.5,"mem":157286}\n'
    ),
    "run2.log": (
        '{"timestamp":"2023-06-01T11:00:00Z","cpu":50.0,"mem":262144}\n'
        '{"timestamp":"2023-06-01T11:00:05Z","cpu":65.0,"mem":524288}\n'
        '{"timestamp":"2023-06-01T11:00:10Z","cpu":55.0,"mem":393216}\n'
        '{"timestamp":"2023-06-01T11:00:15Z","cpu":70.0,"mem":458752}\n'
    ),
    "run3.log": (
        '{"timestamp":"2023-06-01T12:00:00Z","cpu":15.0,"mem":131072}\n'
        '{"timestamp":"2023-06-01T12:00:05Z","cpu":20.0,"mem":196608}\n'
        '{"timestamp":"2023-06-01T12:00:10Z","cpu":25.0,"mem":262144}\n'
        '{"timestamp":"2023-06-01T12:00:15Z","cpu":18.0,"mem":327680}\n'
        '{"timestamp":"2023-06-01T12:00:20Z","cpu":22.0,"mem":393216}\n'
    ),
}


def _read_utf8(path: pathlib.Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        pytest.fail(f"{path} is not valid UTF-8: {exc}")


@pytest.mark.parametrize("filename,expected", EXPECTED_CONTENTS.items())
def test_log_file_exact_content(filename, expected):
    """The seed files must not be altered."""
    path = RAW_DIR / filename
    content = _read_utf8(path)
    assert (
        content == expected
    ), f"Contents of {path} do not match the expected seed data."


# ---------------------------------------------------------------------------
# 3. Per-line JSON structure & field order
# ---------------------------------------------------------------------------

# Regex for quick structural validation (strict spacing)
_LINE_RE = re.compile(
    r'^\{"timestamp":"[^"]+","cpu":[0-9]+(?:\.[0-9]+)?,"mem":[0-9]+\}$'
)


def test_each_line_is_valid_json_with_required_keys_in_order():
    """Every line must be a standalone JSON object with keys in the right order."""
    for path in RAW_DIR.glob("*.log"):
        for lineno, raw_line in enumerate(_read_utf8(path).splitlines(), start=1):
            assert _LINE_RE.match(
                raw_line
            ), f"{path}:{lineno} is not in the expected JSON format."

            # Parse to ensure the JSON is syntactically correct
            obj = json.loads(raw_line)

            # Keys must appear exactly in this order: timestamp, cpu, mem
            assert list(obj.keys()) == [
                "timestamp",
                "cpu",
                "mem",
            ], f"{path}:{lineno} JSON keys are out of order or missing."

            # Basic type checks
            assert isinstance(obj["timestamp"], str), f"{path}:{lineno} timestamp not str"
            assert isinstance(
                obj["cpu"], (int, float)
            ), f"{path}:{lineno} cpu not number"
            assert isinstance(obj["mem"], int), f"{path}:{lineno} mem not int"