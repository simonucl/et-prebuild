# test_initial_state.py
#
# This pytest module verifies the pristine state of the workstation
# *before* the learner runs any commands.  It checks that the services
# registry exists exactly where expected and that its contents match the
# scenario described in the exercise.
#
# The tests purposefully DO NOT look for the output file
# (/home/user/services/active_services.csv) because that file is meant to
# be created by the learner.

import pathlib
import re
import pytest

SERVICES_DIR = pathlib.Path("/home/user/services")
REGISTRY_FILE = SERVICES_DIR / "registry.txt"

# Expected records: (service_name, port_number, status)
EXPECTED_REGISTRY = [
    ("webapp",   "8080", "up"),
    ("auth",     "9090", "up"),
    ("payments", "7070", "down"),
    ("monitor",  "8181", "up"),
    ("search",   "9200", "down"),
    ("cache",    "6379", "up"),
]


def _parse_registry(path):
    """
    Parse the registry file and return a list of tuples
    (service_name, port, status).

    Leading/trailing spaces and tabs are ignored.  Empty lines are skipped.
    """
    records = []
    with path.open(encoding="utf-8") as fh:
        for lineno, raw in enumerate(fh, 1):
            line = raw.strip()
            if not line:
                # Skip blank lines (in case the file ends with an empty line)
                continue

            # The spec guarantees tab-separated values, but allow any
            # whitespace just to be tolerant of accidental spaces.
            parts = re.split(r"[\t ]+", line)
            if len(parts) != 3:
                pytest.fail(
                    f"Line {lineno} in {path} should contain exactly 3 columns "
                    f"(service\\tport\\tstatus).  Found: {parts}"
                )
            records.append(tuple(parts))
    return records


def test_services_directory_exists():
    assert SERVICES_DIR.exists(), (
        f"The directory {SERVICES_DIR} is missing.  "
        "Create it before proceeding."
    )
    assert SERVICES_DIR.is_dir(), (
        f"The path {SERVICES_DIR} exists but is not a directory."
    )


def test_registry_file_exists():
    assert REGISTRY_FILE.exists(), (
        f"The registry file {REGISTRY_FILE} is missing.  "
        "It must be present before you start."
    )
    assert REGISTRY_FILE.is_file(), (
        f"The path {REGISTRY_FILE} exists but is not a regular file."
    )


def test_registry_file_contents():
    # Parse actual records
    actual_records = _parse_registry(REGISTRY_FILE)

    # Build look-up dict: service_name -> (port, status)
    actual_dict = {name: (port, status) for name, port, status in actual_records}

    # 1. Check that every expected service is present with the correct data.
    for exp_name, exp_port, exp_status in EXPECTED_REGISTRY:
        assert exp_name in actual_dict, (
            f"Service '{exp_name}' is missing from {REGISTRY_FILE}."
        )

        act_port, act_status = actual_dict[exp_name]
        assert act_port == exp_port, (
            f"Service '{exp_name}' should have port '{exp_port}' "
            f"but found '{act_port}' in {REGISTRY_FILE}."
        )
        assert act_status == exp_status, (
            f"Service '{exp_name}' should have status '{exp_status}' "
            f"but found '{act_status}' in {REGISTRY_FILE}."
        )

    # 2. Ensure no extra, unexpected services are present.
    expected_names = {name for name, _, _ in EXPECTED_REGISTRY}
    unexpected = set(actual_dict).difference(expected_names)
    assert not unexpected, (
        f"The registry file contains unexpected service(s): {', '.join(sorted(unexpected))}."
    )

    # 3. Sanity check: The file must contain exactly the expected number of records.
    assert len(actual_records) == len(EXPECTED_REGISTRY), (
        f"{REGISTRY_FILE} should contain exactly {len(EXPECTED_REGISTRY)} "
        f"records but contains {len(actual_records)}."
    )