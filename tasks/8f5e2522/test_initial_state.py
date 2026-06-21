# test_initial_state.py
#
# This pytest file validates the **initial** state of the filesystem
# before the student begins the task.  It deliberately does **not**
# look for any of the files that the student is expected to create
# later on.

import os
import pathlib
import re

import pytest

HOME = pathlib.Path("/home/user")
DATA_DIR = HOME / "data"
RAW_FILE = DATA_DIR / "raw_train.tsv"


def test_data_directory_exists():
    assert DATA_DIR.exists(), f"Required directory {DATA_DIR} is missing."
    assert DATA_DIR.is_dir(), f"{DATA_DIR} exists but is not a directory."
    # Basic permission sanity-check: should be readable & writable by the user.
    mode = DATA_DIR.stat().st_mode
    assert mode & 0o700, f"{DATA_DIR} should be user-readable/writable/executable."


def test_raw_train_file_exists():
    assert RAW_FILE.exists(), f"Required file {RAW_FILE} is missing."
    assert RAW_FILE.is_file(), f"{RAW_FILE} exists but is not a regular file."
    assert os.access(RAW_FILE, os.R_OK), f"{RAW_FILE} is not readable."


def test_raw_file_format_and_content():
    """
    Validate that /home/user/data/raw_train.tsv exactly matches the
    specification given in the task description.
    """
    with RAW_FILE.open("r", newline="") as fh:
        lines = fh.readlines()

    # 1. Exactly 4 lines: 1 header + 3 data lines
    assert len(lines) == 4, (
        f"{RAW_FILE} should contain 4 lines (1 header + 3 data), "
        f"but contains {len(lines)}."
    )

    # 2. Every line must end with a UNIX newline '\n' (no CRLF, no missing newline)
    for idx, line in enumerate(lines, start=1):
        assert line.endswith("\n"), f"Line {idx} in {RAW_FILE} does not end with '\\n'."
        assert not line.endswith("\r\n"), (
            f"Line {idx} in {RAW_FILE} ends with Windows newline '\\r\\n'; "
            "UNIX newline '\\n' expected."
        )

    # 3. Header validation
    header_expected = [
        "label",
        "sepal_length",
        "sepal_width",
        "petal_length",
    ]
    header_actual = lines[0].rstrip("\n").split("\t")
    assert header_actual == header_expected, (
        "Header mismatch in raw_train.tsv.\n"
        f"Expected (tab-separated): {header_expected}\n"
        f"Found                 : {header_actual}"
    )

    # Pre-compile a small helper regex for floating-point validation
    float_re = re.compile(r"^[0-9]+(\.[0-9]+)?$")

    # 4. Validate each data line
    expected_labels = {
        "Iris-setosa",
        "Iris-versicolor",
        "Iris-virginica",
    }
    for lineno, raw_line in enumerate(lines[1:], start=2):
        line = raw_line.rstrip("\n")
        # There must be exactly 3 TAB characters → 4 fields
        assert line.count("\t") == 3, (
            f"Line {lineno} in {RAW_FILE} must contain exactly 4 TAB-separated "
            f"fields, but {line.count(chr(9)) + 1} fields were found."
        )

        fields = line.split("\t")
        label, sepal_len, sepal_wid, petal_len = fields

        # Label sanity check
        assert label in expected_labels, (
            f"Unexpected label '{label}' on line {lineno} of {RAW_FILE}."
        )

        # Numeric fields must be valid floats (no extra whitespace)
        for col_name, value in zip(
            ("sepal_length", "sepal_width", "petal_length"),
            (sepal_len, sepal_wid, petal_len),
        ):
            assert float_re.match(value), (
                f"Field '{col_name}' on line {lineno} "
                f"should be a numeric value but got '{value}'."
            )

        # Ensure that re-joining the fields with a single TAB reproduces
        # the original line exactly (guarantees no extra/missing whitespace).
        assert "\t".join(fields) == line, (
            f"Line {lineno} in {RAW_FILE} contains unexpected whitespace."
        )