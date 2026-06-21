# test_initial_state.py
#
# This pytest suite validates that the expected *initial* filesystem layout
# is present **before** students begin working on the assignment.
#
# IMPORTANT:  These tests purposefully avoid looking for any files that
# students are expected to create (e.g. /home/user/report_versions.sh or
# /home/user/version_report.log).  Only the pre-existing resources are
# checked.

from pathlib import Path
import pytest

HOME = Path("/home/user")
MICROSERVICES_DIR = HOME / "microservices"

# Expected services and the exact version strings they must contain.
EXPECTED_SERVICES = {
    "service-alpha": "1.0.0",
    "service-beta": "2.1.3",
}


def test_microservices_directory_exists():
    """
    The root microservices directory must exist and be a directory.
    """
    assert MICROSERVICES_DIR.exists(), (
        f"Expected directory {MICROSERVICES_DIR} does not exist."
    )
    assert MICROSERVICES_DIR.is_dir(), (
        f"Expected {MICROSERVICES_DIR} to be a directory."
    )


@pytest.mark.parametrize("service,expected_version", EXPECTED_SERVICES.items())
def test_each_service_directory_and_version_file(service, expected_version):
    """
    For every predefined microservice ensure:
      1. The service directory exists.
      2. A version.txt file is present.
      3. The version.txt file contains the exact semantic version string.
    """
    service_dir = MICROSERVICES_DIR / service
    version_file = service_dir / "version.txt"

    # 1. Directory existence
    assert service_dir.exists(), (
        f"Missing expected service directory: {service_dir}"
    )
    assert service_dir.is_dir(), (
        f"Expected {service_dir} to be a directory."
    )

    # 2. version.txt existence
    assert version_file.exists(), (
        f"Missing expected file: {version_file}"
    )
    assert version_file.is_file(), (
        f"Expected {version_file} to be a regular file."
    )

    # 3. Content verification
    try:
        raw = version_file.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        pytest.fail(f"Could not decode {version_file} as UTF-8: {exc}")

    # Strip only a single trailing newline for leniency; nothing else.
    content = raw.rstrip("\n")
    assert content == expected_version, (
        f"Incorrect content in {version_file!s}.\n"
        f"Expected: {expected_version!r}\nFound:    {content!r}"
    )