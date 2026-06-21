# test_initial_state.py
#
# This test-suite validates that the required *input* artefacts are present
# and well-formed **before** the student begins the task.  It purposefully
# avoids any reference to the output targets (/home/user/clean_data/ …).
#
# The suite checks:
#   • The compressed archive exists at the expected absolute path.
#   • The archive is a valid gzip’ed tar file that can be opened.
#   • The archive contains exactly the three expected log files in the
#     logs/ sub-directory.
#   • Every line in every bundled *.log file can be decoded as UTF-8 and
#     matches the required tab-delimited schema.
#
# Failures emit clear, prescriptive messages so the learner knows what is
# missing or malformed.

import os
import re
import tarfile
from pathlib import PurePosixPath

import pytest

ARCHIVE_PATH = "/home/user/datasets/log_archive.tar.gz"
EXPECTED_MEMBERS = [
    "logs/app1.log",
    "logs/app2.log",
    "logs/app3.log",
]

# Regex for an individual log line.
#   YYYY-MM-DD<space>HH:MM:SS<TAB>LEVEL<TAB>MODULE<TAB>MESSAGE
LOG_LINE_REGEX = re.compile(
    r"^\d{4}-\d{2}-\d{2} "        # Date  YYYY-MM-DD and a single space
    r"\d{2}:\d{2}:\d{2}\t"        # Time  HH:MM:SS followed by a TAB
    r"[A-Z]+\t"                   # LEVEL (e.g., ERROR, INFO) followed by TAB
    r"[A-Za-z0-9_]+\t"            # MODULE name followed by TAB
    r".*$"                        # MESSAGE (free text until EOL)
)


@pytest.fixture(scope="session")
def opened_tar():
    """
    Yields an opened tarfile object for the log archive.
    The fixture fails early if the file is missing or unreadable.
    """
    assert os.path.exists(ARCHIVE_PATH), (
        f"Required archive not found at: {ARCHIVE_PATH}"
    )
    assert os.path.isfile(ARCHIVE_PATH), (
        f"Expected a file at {ARCHIVE_PATH}, but something else was found."
    )

    try:
        tf = tarfile.open(ARCHIVE_PATH, mode="r:gz")
    except tarfile.TarError as exc:
        pytest.fail(f"Unable to open {ARCHIVE_PATH} as a gzip'ed tar file: {exc}")

    yield tf
    tf.close()


def test_archive_contains_expected_members(opened_tar):
    """
    Ensure the archive has *exactly* the three required log files in logs/.
    Extra files are tolerated but missing files are not.
    """
    member_names = [PurePosixPath(m.name).as_posix() for m in opened_tar.getmembers()]

    # Check presence of expected files.
    missing = [m for m in EXPECTED_MEMBERS if m not in member_names]
    assert not missing, (
        "The following expected log files are missing from the archive: "
        f"{', '.join(missing)}"
    )

    # Also verify that each expected member is a regular file (not a directory).
    irregular = [
        m for m in EXPECTED_MEMBERS
        if not opened_tar.getmember(m).isfile()
    ]
    assert not irregular, (
        "The following paths exist but are not regular files inside the archive: "
        f"{', '.join(irregular)}"
    )


def _iter_log_lines(tar: tarfile.TarFile, member_name: str):
    """
    Yields decoded UTF-8 lines (stripped of trailing newlines) from a given tar member.
    """
    member = tar.getmember(member_name)
    f = tar.extractfile(member)
    if f is None:
        pytest.fail(f"Failed to extract {member_name} from {ARCHIVE_PATH}")
    with f:
        for raw_line in f:
            try:
                yield raw_line.decode("utf-8").rstrip("\n")
            except UnicodeDecodeError as exc:
                pytest.fail(
                    f"File {member_name} contains non-UTF-8 bytes: {exc}"
                )


@pytest.mark.parametrize("member_name", EXPECTED_MEMBERS)
def test_each_line_matches_schema(opened_tar, member_name):
    """
    Verify that every line across all bundled logs strictly follows the
    required tab-delimited schema and is UTF-8 decodable.
    """
    for line_no, line in enumerate(_iter_log_lines(opened_tar, member_name), start=1):
        assert LOG_LINE_REGEX.fullmatch(line), (
            f"Schema mismatch in {member_name} at line {line_no!r}: {line!r}\n"
            "Each line must match "
            "'YYYY-MM-DD HH:MM:SS<TAB>LEVEL<TAB>MODULE<TAB>MESSAGE'"
        )