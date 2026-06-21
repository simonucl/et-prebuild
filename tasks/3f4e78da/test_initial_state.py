# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state that must be
# present BEFORE the student starts working on the task.  It deliberately
# ignores any of the artefacts the student is expected to create
# (merged.csv, merged.json, analysis.log) and focuses solely on the required
# source material.
#
# Requirements being asserted:
#   1. The directory /home/user/docs/meta/ exists and is a directory.
#   2. Two CSV files are present under that directory:
#        - /home/user/docs/meta/part1.csv
#        - /home/user/docs/meta/part2.csv
#   3. Each file’s *entire* textual content matches the specification
#      provided in the task description, byte-for-byte (including the
#      trailing newline).
#
# Any failure message is written to be explicit so that a learner can see
# exactly which precondition is not satisfied.
#
# Only stdlib + pytest are used, as required.
#
# ------------------------------------------------------------------------

import os
from pathlib import Path

import pytest

META_DIR = Path("/home/user/docs/meta")

# Expected raw file contents (including the final newline).
EXPECTED_PART1 = (
    "doc_id,title,topic\n"
    "101,Installation Guide,Setup\n"
    "102,User Manual,Usage\n"
    "103,Troubleshooting,Troubleshooting\n"
    "105,API Reference,API\n"
)
EXPECTED_PART2 = (
    "doc_id,title,topic\n"
    "102,User Manual,Usage\n"
    "104,Release Notes,Release\n"
    "106,FAQ,Support\n"
    "101,Installation Guide,Setup\n"
)

@pytest.mark.dependency(name="meta_dir_exists")
def test_meta_directory_exists():
    assert META_DIR.exists(), f"Required directory {META_DIR} does not exist."
    assert META_DIR.is_dir(), f"Expected {META_DIR} to be a directory."


@pytest.mark.dependency(name="part_files_exist", depends=["meta_dir_exists"])
@pytest.mark.parametrize(
    "filename",
    ["part1.csv", "part2.csv"],
)
def test_part_files_exist(filename):
    file_path = META_DIR / filename
    assert file_path.exists(), f"Required file {file_path} is missing."
    assert file_path.is_file(), f"{file_path} exists but is not a regular file."


@pytest.mark.dependency(depends=["part_files_exist"])
@pytest.mark.parametrize(
    ("filename", "expected_content"),
    [
        ("part1.csv", EXPECTED_PART1),
        ("part2.csv", EXPECTED_PART2),
    ],
)
def test_part_file_content_exact_match(filename, expected_content):
    """
    The content of each part*.csv must match EXACTLY what is specified in the
    task description, including newlines and casing.  A byte-for-byte comparison
    is performed to avoid any accidental deviations.
    """
    file_path = META_DIR / filename
    with open(file_path, "r", encoding="utf-8") as fp:
        actual = fp.read()

    # Provide a helpful diff-style hint if the content is wrong.
    assert (
        actual == expected_content
    ), (
        f"Content mismatch in {file_path}.\n"
        f"--- expected\n{expected_content!r}\n"
        f"+++ actual\n{actual!r}"
    )