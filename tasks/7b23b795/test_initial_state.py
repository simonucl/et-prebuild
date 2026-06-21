# test_initial_state.py
#
# Pytest suite that validates the required **initial** operating-system /
# filesystem state for the “migration plan” task.  It checks for the exact
# presence and content of the three input files that must already exist
# _before_ the student performs any action.  Nothing about the yet-to-be
# produced output files is tested here.

from pathlib import Path
import pytest


HOME = Path("/home/user")
MIGRATION_DIR = HOME / "migration"

PROD_FILE = MIGRATION_DIR / "prod_services.csv"
STAGING_FILE = MIGRATION_DIR / "staging_services.csv"
IPS_FILE = MIGRATION_DIR / "new_cluster_ips.txt"


@pytest.fixture(scope="module")
def prod_expected_lines():
    return [
        "service_id,service_name,current_env,replicas,owner",
        "svc-101,auth-service,production,3,team-login",
        "svc-102,billing-service,production,2,team-payment",
        "svc-103,search-service,production,4,team-search",
    ]


@pytest.fixture(scope="module")
def staging_expected_lines():
    return [
        "service_id,service_name,current_env,replicas,owner",
        "svc-201,auth-service,staging,1,team-login",
        "svc-202,billing-service,staging,1,team-payment",
    ]


@pytest.fixture(scope="module")
def ips_expected_lines():
    return [
        "10.240.0.10",
        "10.240.0.11",
        "10.240.0.12",
        "10.240.0.13",
        "10.240.0.14",
    ]


def _read_file_lines(path: Path):
    """
    Read a file and return its content split into lines _without_ the
    trailing newline characters.  The .strip() is used to ensure that a
    single trailing newline at EOF does not break the comparison, but
    internal newlines are preserved.
    """
    return path.read_text(encoding="utf-8").strip().splitlines()


def test_migration_directory_exists():
    assert MIGRATION_DIR.is_dir(), (
        f"Required directory {MIGRATION_DIR} is missing. "
        "The migration exercise expects this directory to exist."
    )


def test_input_files_exist():
    for path in (PROD_FILE, STAGING_FILE, IPS_FILE):
        assert path.is_file(), (
            f"Required input file {path} is missing. "
            "Make sure the provided dataset is in place."
        )


def test_prod_services_file_content(prod_expected_lines):
    actual = _read_file_lines(PROD_FILE)
    assert actual == prod_expected_lines, (
        f"{PROD_FILE} does not match the expected contents.\n\n"
        "Expected:\n"
        + "\n".join(prod_expected_lines)
        + "\n\nActual:\n"
        + "\n".join(actual)
    )


def test_staging_services_file_content(staging_expected_lines):
    actual = _read_file_lines(STAGING_FILE)
    assert actual == staging_expected_lines, (
        f"{STAGING_FILE} does not match the expected contents.\n\n"
        "Expected:\n"
        + "\n".join(staging_expected_lines)
        + "\n\nActual:\n"
        + "\n".join(actual)
    )


def test_new_cluster_ips_file_content(ips_expected_lines):
    actual = _read_file_lines(IPS_FILE)
    assert actual == ips_expected_lines, (
        f"{IPS_FILE} does not match the expected contents.\n\n"
        "Expected:\n"
        + "\n".join(ips_expected_lines)
        + "\n\nActual:\n"
        + "\n".join(actual)
    )


def test_row_and_line_counts(
    prod_expected_lines, staging_expected_lines, ips_expected_lines
):
    # Exclude header row for CSV counts
    prod_rows = len(prod_expected_lines) - 1
    staging_rows = len(staging_expected_lines) - 1
    total_services = prod_rows + staging_rows
    ip_lines = len(ips_expected_lines)

    assert prod_rows == 3, "prod_services.csv must contain exactly 3 data rows."
    assert staging_rows == 2, "staging_services.csv must contain exactly 2 data rows."
    assert ip_lines == 5, "new_cluster_ips.txt must contain exactly 5 IP addresses."
    assert (
        ip_lines >= total_services
    ), "The IP pool must be at least as large as the total number of services."