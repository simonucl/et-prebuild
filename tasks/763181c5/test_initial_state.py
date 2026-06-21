# test_initial_state.py
#
# Pytest suite that validates the INITIAL operating-system / filesystem state
# before the student performs any actions for the “repos-inventory” exercise.
#
# What we assert:
#   • /home/user/repos-inventory exists and is a directory.
#   • /home/user/repos-inventory/artifacts.tsv exists and its content matches the
#     exact reference data provided in the task description (11 lines: 1 header
#     + 10 data rows, all TAB-separated, Unix LF endings, no carriage returns).
#   • The to-be-created output files curated_artifacts.txt and
#     big_artifacts.log do NOT yet exist.
#
# Only stdlib and pytest are used.

import os
from pathlib import Path

BASE_DIR = Path("/home/user/repos-inventory")
INPUT_FILE = BASE_DIR / "artifacts.tsv"
OUTPUT_CURATED = BASE_DIR / "curated_artifacts.txt"
OUTPUT_BIG = BASE_DIR / "big_artifacts.log"

# Expected content of artifacts.tsv, including newline characters.
EXPECTED_LINES = [
    "repo_id\tartifact_name\tversion\tsize_kb\tsha256\n",
    "core\tcom.acme:libcrypto\t1.2.0\t8640\t7b5f96b26d9f5a37c1e420a63daa45f64f1ac2f9d8bded0372cd5152c3d9d7c1\n",
    "core\tcom.acme:libhttp\t2.5.1\t12800\t3cfc7dbeab9e4d0482a6f8f2dfe6d1b62a6e2ce4b3c0e5e4b21dd9c649c34337\n",
    "utils\torg.tools:zipper\t0.9.8\t5120\td7a4b5a8934dd94dcd4b4a6e4b3e2c8fd2e9adf3edd5c6b1b3a9e5d8f6a7b2d3\n",
    "utils\torg.tools:packer\t1.0.0\t20480\te6f2d3b4a5c6979876543210abcdefabcdef01234567890fedcba9876543210\n",
    "ml\tai.deep:torch\t1.9.0\t73400\tc1d2e3f40506070809101112131415161718191a1b1c1d1e1f20212223242526\n",
    "ml\tai.deep:onnx\t1.8.1\t9200\taabbccddeeff00112233445566778899aabbccddeeff00112233445566778899\n",
    "java\torg.apache:log4j\t2.14.1\t800\t99887766554433221100ffeeddccbbaa99887766554433221100ffeeddccbbaa\n",
    "java\tcom.google:guava\t30.1.1\t2650\t11223344556677889900aabbccddeeff00112233445566778899aabbccddeeff\n",
    "db\tcom.mysql:mysql-connector\t8.0.25\t9800\t2233445566778899aabbccddeeff00112233445566778899aabbccddeeff\n",
    "db\torg.postgres:pgjdbc\t42.2.20\t5020\t33445566778899aabbccddeeff00112233445566778899aabbccddeeff00\n",
]


def test_repos_inventory_directory_exists():
    assert BASE_DIR.exists(), f"Directory {BASE_DIR} is missing."
    assert BASE_DIR.is_dir(), f"{BASE_DIR} exists but is not a directory."


def test_artifacts_file_exists():
    assert INPUT_FILE.exists(), f"Required input file {INPUT_FILE} is missing."
    assert INPUT_FILE.is_file(), f"{INPUT_FILE} exists but is not a regular file."


def test_artifacts_file_content_exact_match():
    """Ensure artifacts.tsv content matches the reference exactly."""
    with INPUT_FILE.open("rb") as fh:
        raw = fh.read()

    # The last byte must be a single LF (10). No CR (13) characters allowed.
    assert raw.endswith(b"\n"), (
        f"{INPUT_FILE} must end with a single LF newline."
    )
    assert b"\r" not in raw, (
        f"{INPUT_FILE} must use Unix LF newlines only; CR characters found."
    )

    lines = raw.decode("utf-8").splitlines(keepends=True)
    assert lines == EXPECTED_LINES, (
        "Content of artifacts.tsv does not match the expected reference data. "
        f"Differences:\nEXPECTED:\n{''.join(EXPECTED_LINES)}\n"
        f"FOUND:\n{''.join(lines)}"
    )


def test_output_files_do_not_yet_exist():
    assert not OUTPUT_CURATED.exists(), (
        f"{OUTPUT_CURATED} should NOT exist before the task is performed."
    )
    assert not OUTPUT_BIG.exists(), (
        f"{OUTPUT_BIG} should NOT exist before the task is performed."
    )