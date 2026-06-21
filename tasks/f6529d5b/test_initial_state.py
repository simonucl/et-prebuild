# test_initial_state.py
"""
Pytest suite verifying the pristine filesystem state *before* the student’s
checksum-audit script is executed.

These tests assert that:
1. /home/user/source_files/ exists and is a directory.
2. Exactly three regular files live immediately inside that directory.
3. Each required file exists and its byte-content is *exactly* as documented
   in the task description.
4. The compressed artefact decompresses to the expected payload.

NOTE:
• We purposely do NOT test for the presence or absence of any output artefacts
  (e.g. /home/user/audit_2023Q4/), as they are to be created by the student.
• Only stdlib and pytest are used.
"""

import os
import stat
import gzip
import pytest

SRC_DIR = "/home/user/source_files"
EXPECTED_FILES = sorted(
    [
        "financials_Q4.csv",
        "policy_doc.txt",
        "infra_snapshot.tar.gz",
    ]
)

# Expected byte-contents for the two text files (including trailing newlines)
EXPECTED_CONTENTS = {
    "financials_Q4.csv": (
        b"Dept,Spend,Quarter\n"
        b"IT,23500,Q4\n"
        b"HR,8200,Q4\n"
        b"Finance,12300,Q4\n"
    ),
    "policy_doc.txt": (
        b"All employees must adhere to the security compliance guidelines "
        b"set forth in section 9.2.\n"
    ),
    # infra_snapshot.tar.gz verified via decompression below
}


def test_source_directory_exists_and_is_dir():
    assert os.path.isdir(SRC_DIR), (
        f"Required directory {SRC_DIR} is missing or is not a directory."
    )


def test_source_directory_contents():
    dir_listing = sorted(
        [
            entry
            for entry in os.listdir(SRC_DIR)
            if os.path.isfile(os.path.join(SRC_DIR, entry))
        ]
    )
    assert dir_listing == EXPECTED_FILES, (
        f"{SRC_DIR} must contain exactly the files "
        f"{EXPECTED_FILES}, but contains {dir_listing}."
    )


@pytest.mark.parametrize("filename", ["financials_Q4.csv", "policy_doc.txt"])
def test_text_file_contents_exact(filename):
    path = os.path.join(SRC_DIR, filename)
    assert os.path.isfile(path), f"Missing required file: {path}"
    with open(path, "rb") as fh:
        data = fh.read()
    expected = EXPECTED_CONTENTS[filename]
    assert data == expected, (
        f"Contents of {path} do not match expected bytes.\n"
        f"Expected ({len(expected)} bytes): {expected!r}\n"
        f"Actual   ({len(data)} bytes): {data!r}"
    )


def test_gzip_snapshot_decompresses_correctly():
    filename = "infra_snapshot.tar.gz"
    path = os.path.join(SRC_DIR, filename)
    assert os.path.isfile(path), f"Missing required file: {path}"

    with gzip.open(path, "rb") as gz:
        decompressed = gz.read()

    expected_payload = b"snapshot-2023Q4"
    assert (
        decompressed == expected_payload
    ), "Decompressed payload of infra_snapshot.tar.gz is incorrect."


def test_files_are_regular_and_readable():
    """
    Ensure each expected file is a regular file with read permission for the owner.
    """
    for fname in EXPECTED_FILES:
        path = os.path.join(SRC_DIR, fname)
        st = os.stat(path)
        assert stat.S_ISREG(st.st_mode), f"{path} is not a regular file."
        assert (
            st.st_mode & stat.S_IRUSR
        ), f"Owner does not have read permission on {path}."