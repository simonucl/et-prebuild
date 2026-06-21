# test_initial_state.py
#
# This test-suite validates that the starter filesystem state expected by the
# assignment is present **before** the student performs any work.  In
# particular it checks:
#
#   • Required directories exist and are writable by the current user.
#   • The raw CSV file exists and its contents exactly match the specification.
#
# IMPORTANT:  The tests purposefully do *not* look for any output artefacts
#             such as “clean_sales.csv” or the monitoring logs.  Those will be
#             produced later by the student solution.

import os
from pathlib import Path
import stat
import textwrap

HOME = Path("/home/user")
DATA_DIR = HOME / "data"
MON_DIR = HOME / "monitoring"
RAW_CSV = DATA_DIR / "raw_sales.csv"


def _human_perms(mode: int) -> str:
    """Return a symbolic representation like 'rwx------' for assert msgs."""
    bits = [
        (stat.S_IRUSR, "r"), (stat.S_IWUSR, "w"), (stat.S_IXUSR, "x"),
        (stat.S_IRGRP, "r"), (stat.S_IWGRP, "w"), (stat.S_IXGRP, "x"),
        (stat.S_IROTH, "r"), (stat.S_IWOTH, "w"), (stat.S_IXOTH, "x"),
    ]
    return "".join(flag if mode & bit else "-" for bit, flag in bits)


def test_required_directories_exist_and_are_writable():
    for directory in (DATA_DIR, MON_DIR):
        assert directory.exists(), f"Required directory missing: {directory}"
        assert directory.is_dir(), f"Expected a directory at {directory}"
        # Must be writable by user
        assert os.access(directory, os.W_OK), (
            f"Directory {directory} is not writable by the current user"
        )


def test_raw_sales_csv_exists_with_correct_contents():
    assert RAW_CSV.exists(), (
        f"The raw dataset {RAW_CSV} is missing. "
        "It must be present before the cleaning step."
    )
    assert RAW_CSV.is_file(), f"Expected {RAW_CSV} to be a file, not a directory."

    # Read file using universal newlines for robustness.
    with RAW_CSV.open(newline="") as fp:
        content = fp.read()

    # Normalize to Unix LF endings for comparison; the assignment requires
    # consistency in the sample provided, which uses LF.
    content_lf = content.replace("\r\n", "\n").rstrip("\n")
    expected = textwrap.dedent("""\
        id,product,price,quantity
        1,Widget,19.99,5
        2,Gadget,,3
        3,Thingamabob,4.99,
        4,Widget,19.99,2
        5,Gizmo,8.49,0""")

    assert content_lf == expected, (
        "The contents of raw_sales.csv do not match the expected starter data.\n\n"
        "Expected:\n"
        f"{expected}\n\n"
        "Found:\n"
        f"{content_lf}"
    )

    # Additional sanity: confirm the header and that we have 6 total lines.
    lines = content_lf.split("\n")
    assert lines[0] == "id,product,price,quantity", "Header row is incorrect."
    assert len(lines) == 6, (
        f"raw_sales.csv should contain exactly 6 lines (1 header + 5 data) "
        f"but contains {len(lines)}."
    )