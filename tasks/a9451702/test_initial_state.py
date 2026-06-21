# test_initial_state.py
#
# Pytest suite verifying the *initial* operating-system / filesystem
# state before the student performs any action for the “evidence bundle”
# exercise.
#
# Rules respected:
#   • Only stdlib + pytest are used.
#   • We check *only* the files that must exist **before** the task
#     begins (nothing that the student has to create).
#   • Any failure message is explicit about what is missing / wrong.
#   • Absolute paths are used for all filesystem checks.

import os
import tarfile
import pytest

HOME = "/home/user"
EVIDENCE_DIR = os.path.join(HOME, "evidence")
BUNDLE_PATH = os.path.join(EVIDENCE_DIR, "evidence_bundle.tar.gz")

# Expected members inside the archive (files only, directories ignored)
EXPECTED_FILE_MEMBERS = [
    "auth.log.2023-08-11",
    "syslog.2023-08-11",
    "nginx/access.log",
    "nginx/error.log",
]

# Exact expected contents for each regular file in the archive
EXPECTED_FILE_CONTENTS = {
    "auth.log.2023-08-11": (
        "Aug 11 02:15:47 sshd[2318]: Accepted password for analyst from "
        "10.0.0.42 port 55218 ssh2\n"
    ),
    "syslog.2023-08-11": (
        "Aug 11 02:16:02 kernel: audit: type=1105 msg=audit(1691727362.123:98): "
        "audit_pid=1 ...\n"
    ),
    "nginx/access.log": (
        '10.0.0.17 - - [11/Aug/2023:02:17:03 +0000] "GET /index.html HTTP/1.1" '
        '200 612 "-" "curl/7.58.0"\n'
    ),
    "nginx/error.log": (
        '2023/08/11 02:17:07 [error] 5342#0: *1 open() "/var/www/html/favicon.ico" '
        'failed (2: No such file or directory)...\n'
    ),
}


def test_evidence_directory_exists():
    assert os.path.isdir(EVIDENCE_DIR), (
        f"Required directory '{EVIDENCE_DIR}' is missing. "
        "The exercise cannot proceed without it."
    )


def test_bundle_exists_and_is_file():
    assert os.path.isfile(BUNDLE_PATH), (
        f"Evidence bundle '{BUNDLE_PATH}' is missing. "
        "Ensure the gzip-compressed tar archive is present."
    )


@pytest.fixture(scope="module")
def opened_tar():
    """Open the gzip-compressed tar archive once for all tests."""
    try:
        with tarfile.open(BUNDLE_PATH, "r:gz") as tf:
            # Reopen with mode 'r:gz' each time needed; returning the path
            # ensures isolation (tarfile objects are not re-entrant).
            pass
    except tarfile.TarError as exc:
        pytest.fail(f"Archive '{BUNDLE_PATH}' cannot be opened as a gzip tar: {exc}")

    # Provide the path; individual tests will open as needed
    return BUNDLE_PATH


def get_regular_members(tf: tarfile.TarFile):
    """Return list of TarInfo objects that are regular files (not directories)."""
    return [m for m in tf.getmembers() if m.isfile()]


def test_archive_contains_expected_files_only(opened_tar):
    with tarfile.open(opened_tar, "r:gz") as tf:
        member_names = sorted(m.name for m in get_regular_members(tf))

    assert member_names == sorted(EXPECTED_FILE_MEMBERS), (
        "The evidence archive does not contain the expected set of files.\n"
        f"Expected (sorted): {sorted(EXPECTED_FILE_MEMBERS)}\n"
        f"Found    (sorted): {member_names}"
    )


@pytest.mark.parametrize("member_name", EXPECTED_FILE_MEMBERS)
def test_each_file_content_matches_expected(opened_tar, member_name):
    expected_content = EXPECTED_FILE_CONTENTS[member_name]
    with tarfile.open(opened_tar, "r:gz") as tf:
        try:
            extracted = tf.extractfile(member_name)
        except KeyError:
            pytest.fail(
                f"Expected file '{member_name}' not found inside the archive."
            )
        assert extracted is not None, (
            f"Unable to extract '{member_name}' from the archive."
        )
        content_bytes = extracted.read()
        try:
            content_str = content_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            pytest.fail(
                f"File '{member_name}' is not valid UTF-8 as required: {exc}"
            )

    assert content_str == expected_content, (
        f"Content mismatch for '{member_name}'.\n"
        "---- expected ----\n"
        f"{expected_content!r}\n"
        "---- actual ----\n"
        f"{content_str!r}"
    )