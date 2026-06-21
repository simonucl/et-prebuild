# test_initial_state.py
#
# This test-suite verifies that the operating-system / filesystem is in the
# expected **initial** state _before_ the student runs any commands.
#
# What we check:
#   • /home/user/artifacts exists and is a directory.
#   • The two APK files are present.
#   • The APK files’ SHA-256 digests are exactly as documented.
#   • /home/user/artifacts/expected_checksums.sha256 exists, contains exactly
#     two lines in the correct “sha256␠␠filename” format and the digests inside
#     match the actual APK digests.
#
# What we DO NOT check (because those are outputs the student must create):
#   • /home/user/artifacts/verification.log or any other result artefact.

import hashlib
import os
import re
from pathlib import Path

import pytest

ARTIFACTS_DIR = Path("/home/user/artifacts")
APK_DEBUG = ARTIFACTS_DIR / "app-debug.apk"
APK_RELEASE = ARTIFACTS_DIR / "app-release.apk"
EXPECTED_FILE = ARTIFACTS_DIR / "expected_checksums.sha256"

# Ground-truth digests for the initial files.
DIGEST_DEBUG = (
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"  # sha256 of 0-byte file
)
DIGEST_RELEASE = (
    "ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb"  # sha256 of literal "a"
)

# --------------------------------------------------------------------------- #
# Helper utilities                                                            #
# --------------------------------------------------------------------------- #
def sha256_of_file(path: Path) -> str:
    """Return the SHA-256 hex digest of *path*."""
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #
def test_artifacts_directory_exists():
    assert ARTIFACTS_DIR.exists(), f"Directory {ARTIFACTS_DIR} is missing."
    assert ARTIFACTS_DIR.is_dir(), f"{ARTIFACTS_DIR} exists but is not a directory."


@pytest.mark.parametrize(
    "path,expected_digest,description",
    [
        (APK_DEBUG, DIGEST_DEBUG, "debug APK"),
        (APK_RELEASE, DIGEST_RELEASE, "release APK"),
    ],
)
def test_apk_files_exist_and_have_expected_digest(path: Path, expected_digest: str, description: str):
    assert path.exists(), f"The {description} file {path} is missing."
    assert path.is_file(), f"The {description} path {path} exists but is not a file."
    actual_digest = sha256_of_file(path)
    assert (
        actual_digest == expected_digest
    ), f"SHA-256 of {path} is {actual_digest}, expected {expected_digest}."


def test_expected_checksums_file_format_and_contents():
    assert EXPECTED_FILE.exists(), f"Expected checksum file {EXPECTED_FILE} is missing."
    assert EXPECTED_FILE.is_file(), f"{EXPECTED_FILE} exists but is not a file."

    content = EXPECTED_FILE.read_text(encoding="utf-8")
    # Ensure file ends with a single LF. Two strategies:
    #   • Must end with '\n'.
    #   • Must not end with '\n\n'.
    assert content.endswith(
        "\n"
    ), f"{EXPECTED_FILE} must end with a single LF (newline)."
    assert not content.endswith(
        "\n\n"
    ), f"{EXPECTED_FILE} must not contain a blank line at the end."

    # Split lines (strip removes the terminal newline we just verified).
    lines = content.rstrip("\n").split("\n")
    assert (
        len(lines) == 2
    ), f"{EXPECTED_FILE} must contain exactly two lines, found {len(lines)}."

    # Regular expression for “64 lowercase hex chars, two spaces, filename”
    pattern = re.compile(r"^[0-9a-f]{64}  ([^\s]+)$")

    digests_in_file = {}
    for idx, line in enumerate(lines, 1):
        m = pattern.match(line)
        assert m, f"Line {idx} in {EXPECTED_FILE} has invalid format: {line!r}"
        filename = m.group(1)
        digest = line.split("  ")[0]
        digests_in_file[filename] = digest

    # Ensure we have entries for both expected APKs.
    for apk_path, expected_digest in [
        (APK_DEBUG, DIGEST_DEBUG),
        (APK_RELEASE, DIGEST_RELEASE),
    ]:
        fname = apk_path.name
        assert (
            fname in digests_in_file
        ), f"{EXPECTED_FILE} is missing an entry for {fname}."
        digest_from_file = digests_in_file[fname]
        assert (
            digest_from_file == expected_digest
        ), f"Digest for {fname} in {EXPECTED_FILE} is {digest_from_file}, expected {expected_digest}."


def test_no_output_files_yet():
    """Ensure we’re checking the initial state only.

    We do NOT require the student’s output yet, but we also must not fail if it
    already exists.  Therefore, this test is intentionally left blank – its
    presence reminds maintainers to never assert on result artefacts here.
    """
    pass