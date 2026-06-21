# test_initial_state.py
#
# This pytest file validates that the initial filesystem state
# needed for the FinOps-log filtering exercise is present and
# correct *before* the student performs any action.
#
# Only the *input* side is checked: we deliberately avoid touching
# the soon-to-be-created “filtered” or “summary” paths.

import pathlib
import pytest

ROOT = pathlib.Path("/home/user/finops")
RAW_DIR = ROOT / "raw"
RAW_LOG = RAW_DIR / "usage-2023-09.log"

EXPECTED_LINES = [
    "2023-09-01T00:05:14Z,ec2,StartInstances,increase,4.27",
    "2023-09-01T00:15:51Z,ec2,StopInstances,decrease,-1.89",
    "2023-09-01T00:45:07Z,s3,PutObject,increase,0.01",
    "2023-09-01T01:12:33Z,rds,CreateDBInstance,increase,1.20",
    "2023-09-01T01:30:05Z,rds,DeleteDBInstance,decrease,-1.20",
    "2023-09-01T02:05:00Z,ec2,RunInstances,increase,6.34",
    "2023-09-01T02:50:49Z,lambda,InvokeFunction,increase,0.0002",
    "2023-09-01T03:15:30Z,ec2,TerminateInstances,decrease,-4.27",
    "2023-09-01T04:22:10Z,rds,ModifyDBInstance,increase,0.58",
    "2023-09-01T05:02:45Z,s3,DeleteObject,decrease,-0.01",
]


def test_raw_directory_exists():
    assert RAW_DIR.is_dir(), (
        f"The directory {RAW_DIR} is missing. "
        "It must exist and contain the raw log to be processed."
    )


def test_raw_log_file_exists_and_has_correct_content():
    assert RAW_LOG.is_file(), (
        f"The log file {RAW_LOG} is missing. "
        "It must be present before you start filtering."
    )

    with RAW_LOG.open("r", encoding="utf-8") as fh:
        lines = [ln.rstrip("\n") for ln in fh.readlines()]

    # Check the number of lines first for a quick sanity check.
    assert len(lines) == len(
        EXPECTED_LINES
    ), f"{RAW_LOG} should have {len(EXPECTED_LINES)} lines, found {len(lines)}."

    # Verify exact content line by line so the student cannot work
    # with an altered input file.
    mismatches = [
        (idx + 1, exp, got)
        for idx, (exp, got) in enumerate(zip(EXPECTED_LINES, lines))
        if exp != got
    ]

    if mismatches:
        msg_lines = ["The contents of the raw log differ from what is expected:"]
        for lineno, exp, got in mismatches:
            msg_lines.append(
                f"  Line {lineno}: expected '{exp}', but found '{got}'."
            )
        pytest.fail("\n".join(msg_lines))