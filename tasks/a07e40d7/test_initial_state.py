# test_initial_state.py
#
# This test-suite verifies that the *initial* state of the filesystem is
# exactly what the assignment description specifies.  It deliberately
# checks only pre-existing artefacts – **NOT** anything that the student
# is asked to create.
#
# Rules enforced:
#   • Expected directory / file layout exists.
#   • The three *.sh files (and only those) are present under
#     /home/user/projects and contain the exact lines that the grader
#     relies on, in the expected 1-based line numbers.
#   • The credential-check output file must NOT exist yet.
#
# Any failure message is crafted to tell the student precisely what is
# missing or different.

import os
from pathlib import Path
import pytest


PROJECT_ROOT = Path("/home/user/projects").resolve()
REPORT_FILE = Path("/home/user/security_report.txt").resolve()


@pytest.fixture(scope="module")
def project_root():
    """Ensure /home/user/projects exists and is a directory."""
    assert PROJECT_ROOT.is_dir(), (
        f"Expected directory {PROJECT_ROOT} to exist, "
        "but it was not found."
    )
    return PROJECT_ROOT


def test_expected_sh_files_exist(project_root):
    """
    Exactly three *.sh files must exist beneath /home/user/projects:

        deploy.sh
        utils/cleanup.sh
        utils/helper.sh
    """
    expected_relative = {
        Path("deploy.sh"),
        Path("utils/cleanup.sh"),
        Path("utils/helper.sh"),
    }

    discovered_relative = {
        p.relative_to(project_root)
        for p in project_root.rglob("*.sh")
        if p.is_file()
    }

    missing = expected_relative - discovered_relative
    unexpected = discovered_relative - expected_relative

    assert not missing, (
        "The following required *.sh files are missing:\n"
        + "\n".join(str(project_root / m) for m in sorted(missing))
    )
    assert not unexpected, (
        "Unexpected *.sh files were found under the project directory.\n"
        "Only the files specified in the task description should exist.\n"
        "Unexpected files:\n"
        + "\n".join(str(project_root / u) for u in sorted(unexpected))
    )


@pytest.mark.parametrize(
    "rel_path, line_no, expected_line",
    [
        # (relative path, 1-based line number, expected entire line content)
        ("deploy.sh", 3, "db_password=secret123"),
        ("utils/cleanup.sh", 2, " password =cleanme"),   # leading space intentional
        ("utils/cleanup.sh", 3, "password=cleanme2"),
        ("utils/helper.sh", 4, "passwd=letmein"),
    ],
)
def test_file_contains_expected_line(project_root, rel_path, line_no, expected_line):
    """
    Verify that each script contains the exact credential line at the
    specified 1-based line number.  Whitespace at the *end* of the line
    is ignored, but everything else must match verbatim.
    """
    file_path = project_root / rel_path
    assert file_path.is_file(), f"Missing expected file: {file_path}"

    with file_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    assert line_no <= len(lines), (
        f"{file_path} should have at least {line_no} lines, "
        f"but it only has {len(lines)}."
    )

    # Strip only trailing newline / carriage return so we can match
    # leading whitespace and internal spaces exactly.
    actual = lines[line_no - 1].rstrip("\r\n")

    assert actual == expected_line, (
        f"Line {line_no} of {file_path} is expected to be:\n"
        f"    {expected_line!r}\n"
        f"but the actual content is:\n"
        f"    {actual!r}"
    )


def test_report_file_does_not_exist_yet():
    """
    The credential scan has not run yet, therefore the report file
    /home/user/security_report.txt must NOT be present.
    """
    assert not REPORT_FILE.exists(), (
        f"The report file {REPORT_FILE} already exists, but it should "
        "be created *after* the student runs their solution."
    )