# test_initial_state.py
#
# This pytest suite validates the *initial* state of the operating system /
# filesystem before the student performs any actions.
#
# It asserts the presence and exact contents of the inventory CSV located at
# /home/user/policies/service_ports.csv.
#
# NOTE: Per spec, we intentionally do NOT test for the presence or absence of
# any output artefacts (e.g., /home/user/output/...)—those will be created by
# the student later.

import os
import pytest
import textwrap

CSV_PATH = "/home/user/policies/service_ports.csv"

# Expected byte-for-byte content of the CSV (including final newline)
EXPECTED_CSV_CONTENT = textwrap.dedent("""\
    service,port
    ssh,22
    http,80
    https,443
    custom-app,8080
    db-mysql,3306
    db-postgres,5432
    old-telnet,23
    custom-admin,10022
    dev-service,12000
""")

def test_service_ports_csv_exists():
    """
    The inventory CSV must exist and be a regular file.
    """
    assert os.path.exists(CSV_PATH), (
        f"Required file not found: {CSV_PATH}"
    )
    assert os.path.isfile(CSV_PATH), (
        f"Expected a regular file at {CSV_PATH}, but something else is there."
    )

def test_service_ports_csv_contents():
    """
    The CSV should match the expected baseline exactly.
    """
    with open(CSV_PATH, "r", encoding="utf-8") as fh:
        contents = fh.read()

    # The expected content string above includes the mandatory trailing newline.
    assert contents == EXPECTED_CSV_CONTENT, (
        "Contents of {path} do not match the expected baseline.\n\n"
        "Expected:\n{expected}\n\nActual:\n{actual}".format(
            path=CSV_PATH,
            expected=repr(EXPECTED_CSV_CONTENT),
            actual=repr(contents)
        )
    )