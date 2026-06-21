# test_initial_state.py
#
# This pytest suite validates the *initial* state of the filesystem
# before the student runs any commands for the “checksum manifest”
# exercise.  It purpose-fully **fails** if anything is missing, extra,
# or already created (e.g. a premature manifest.csv file).

import os
from pathlib import Path
import hashlib

# Absolute paths used throughout the tests
REPO_ROOT = Path("/home/user/artifacts/java").resolve()
LIB_A_JAR = REPO_ROOT / "libraryA-1.0.jar"
PLUGIN_DIR = REPO_ROOT / "plugins"
PLUGIN_B_JAR = PLUGIN_DIR / "pluginB-2.1.jar"
MANIFEST_CSV = REPO_ROOT / "manifest.csv"


def test_repository_root_exists_and_is_directory():
    assert REPO_ROOT.is_dir(), (
        f"Expected repository root directory at '{REPO_ROOT}', "
        "but it does not exist or is not a directory."
    )


def test_expected_jar_files_exist():
    assert LIB_A_JAR.is_file(), f"Missing expected JAR file: '{LIB_A_JAR}'."
    assert PLUGIN_DIR.is_dir(), (
        f"Expected plugins sub-directory at '{PLUGIN_DIR}', "
        "but it is missing or not a directory."
    )
    assert PLUGIN_B_JAR.is_file(), f"Missing expected JAR file: '{PLUGIN_B_JAR}'."


def test_no_manifest_yet():
    assert not MANIFEST_CSV.exists(), (
        f"'{MANIFEST_CSV}' already exists, but it should be created only by "
        "the student’s one-liner command."
    )


def test_no_extra_jar_files_present():
    """
    The repository must contain **only** the two expected .jar files.
    This guards against accidental extra files that would change the
    required manifest content.
    """
    jars_found = sorted(
        str(p.relative_to(REPO_ROOT)) for p in REPO_ROOT.rglob("*.jar")
    )
    expected = sorted(
        [
            "libraryA-1.0.jar",
            "plugins/pluginB-2.1.jar",
        ]
    )
    assert jars_found == expected, (
        "Unexpected set of .jar files present.\n"
        f"Expected: {expected}\n"
        f"Found   : {jars_found}"
    )


def test_jar_file_contents_match_reference():
    """
    Sanity-check the contents so the checksums verified later by the
    autograder are deterministic.
    """
    contents_a = LIB_A_JAR.read_bytes()
    contents_b = PLUGIN_B_JAR.read_bytes()

    assert contents_a == b"Sample binary A\n", (
        f"Contents of '{LIB_A_JAR}' do not match the expected reference bytes."
    )
    assert contents_b == b"Sample binary B\n", (
        f"Contents of '{PLUGIN_B_JAR}' do not match the expected reference bytes."
    )


def test_sha256_checksums_are_stable():
    """
    Compute the SHA-256 of each JAR and ensure the result is exactly 64
    lowercase hex characters.  This does **not** assert specific values
    (the authoritative values live in the evaluation harness), but it
    guarantees that the files are hashable and not empty.
    """
    for jar_path in (LIB_A_JAR, PLUGIN_B_JAR):
        digest = hashlib.sha256(jar_path.read_bytes()).hexdigest()
        assert len(digest) == 64 and digest.islower(), (
            f"SHA-256 digest of '{jar_path}' is malformed: '{digest}'."
        )