# test_initial_state.py

"""
Pytest suite that validates the OS / filesystem state **before** the learner
runs any commands for the “resolve domain -> IPv4” exercise.

What is checked:
1. Presence and permissions of /home/user/data/ directory.
2. Presence, permissions and *exact* content of /home/user/data/domains.csv.
3. Presence and permissions of /home/user/output/ directory
   and that it is completely empty (i.e. the learner has not yet
   created /home/user/output/resolved_domains.csv).

Only stdlib & pytest are used.
"""

import os
import stat
import pytest


DATA_DIR = "/home/user/data"
DOMAINS_CSV = "/home/user/data/domains.csv"
OUTPUT_DIR = "/home/user/output"
RESOLVED_CSV = "/home/user/output/resolved_domains.csv"

EXPECTED_CSV_CONTENT = (
    "domain\n"
    "example.com\n"
    "iana.org\n"
)


def _mode(path):
    "Return permission bits like 0o755 from a path."
    return stat.S_IMODE(os.stat(path).st_mode)


@pytest.mark.dependency(name="data_dir")
def test_data_directory_exists():
    assert os.path.isdir(DATA_DIR), (
        f"Required directory {DATA_DIR} is missing or not a directory."
    )
    expected_perm = 0o755
    actual_perm = _mode(DATA_DIR)
    assert actual_perm == expected_perm, (
        f"{DATA_DIR} permissions are {oct(actual_perm)}, expected {oct(expected_perm)}."
    )


@pytest.mark.dependency(depends=["data_dir"], name="domains_csv")
def test_domains_csv_exists_and_contents():
    assert os.path.isfile(DOMAINS_CSV), (
        f"Required file {DOMAINS_CSV} is missing."
    )

    expected_perm = 0o644
    actual_perm = _mode(DOMAINS_CSV)
    assert actual_perm == expected_perm, (
        f"{DOMAINS_CSV} permissions are {oct(actual_perm)}, expected {oct(expected_perm)}."
    )

    with open(DOMAINS_CSV, "r", encoding="utf-8") as fh:
        content = fh.read()

    assert content == EXPECTED_CSV_CONTENT, (
        f"{DOMAINS_CSV} contents differ from expected.\n"
        "Expected (repr):\n"
        f"{repr(EXPECTED_CSV_CONTENT)}\n"
        "Got (repr):\n"
        f"{repr(content)}"
    )


@pytest.mark.dependency(name="output_dir")
def test_output_directory_exists_and_empty():
    assert os.path.isdir(OUTPUT_DIR), (
        f"Required directory {OUTPUT_DIR} is missing or not a directory."
    )

    expected_perm = 0o755
    actual_perm = _mode(OUTPUT_DIR)
    assert actual_perm == expected_perm, (
        f"{OUTPUT_DIR} permissions are {oct(actual_perm)}, expected {oct(expected_perm)}."
    )

    contents = os.listdir(OUTPUT_DIR)
    assert contents == [] or contents == ['.gitkeep'] and len(contents) == 1, (
        f"{OUTPUT_DIR} is expected to be empty before the task starts; "
        f"found contents: {contents}"
    )

    # Ensure the target artefact is *not* present yet
    assert not os.path.exists(RESOLVED_CSV), (
        f"{RESOLVED_CSV} should not exist before the learner begins."
    )