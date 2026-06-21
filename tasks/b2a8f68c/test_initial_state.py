# test_initial_state.py
#
# Pytest suite that validates the **initial** state of the filesystem
# before the student performs any action for the “service-level network
# audit” exercise.
#
# The checks deliberately avoid looking for any *output* artefacts
# (e.g. /home/user/network_diagnostics or the final log file) because
# those will be created by the student later on.
#
# Only the presence *and* correctness of the Kubernetes manifest
# sources under /home/user/manifests are verified here.
#
# The tests rely solely on the Python standard library + pytest.

import pathlib
import re
from typing import List, Dict

MANIFEST_DIR = pathlib.Path("/home/user/manifests")

EXPECTED_FILES = {
    "web-deployment.yaml",
    "api-gateway.yaml",
    "db.yaml",
}

# Expected “ground-truth” data extracted from the exercise description
TRUTH_SERVICES = {
    "api-gateway": {
        "clusterIP": "10.96.0.20",
        "type": "NodePort",
        "nodePorts": [40000],
    },
    "postgres": {
        "clusterIP": "10.96.0.30",
        "type": "ClusterIP",
        "nodePorts": [],
    },
    "web-service": {
        "clusterIP": "10.96.0.10",
        "type": "NodePort",
        "nodePorts": [30080],
    },
}


# ----------------------------------------------------------------------
# Very small, purposely limited, *ad-hoc* YAML “parser”.
# It is **not** a full YAML implementation – just good enough for the
# specific patterns that occur in the manifests we need to validate.
# ----------------------------------------------------------------------
SERVICE_KINDS = re.compile(r"^\s*kind:\s*Service\s*$")
NAME_RE = re.compile(r"^\s*name:\s*(\S+)\s*$")
CLUSTER_IP_RE = re.compile(r"^\s*clusterIP:\s*(\S+)\s*$")
TYPE_RE = re.compile(r"^\s*type:\s*(\S+)\s*$")
NODEPORT_RE = re.compile(r"^\s*nodePort:\s*(\d+)\s*$")


def parse_services_from_text(text: str) -> List[Dict]:
    """
    Extremely small subset “parser” that returns a list of dictionaries,
    each describing one Service object found in the YAML text.
    We only extract the fields needed for the assertions below.
    """
    services: List[Dict] = []

    docs = text.split("\n---")
    for doc in docs:
        lines = doc.splitlines()

        # First, detect if this document is a Service.
        if not any(SERVICE_KINDS.match(line) for line in lines):
            continue  # skip non-Service documents

        service_data = {
            "name": None,
            "clusterIP": None,
            "type": "ClusterIP",   # default if omitted
            "nodePorts": [],
        }

        # Flags so that we only consider the *first* metadata.name
        seen_name = False

        for line in lines:
            if not seen_name:
                m = NAME_RE.match(line)
                if m:
                    service_data["name"] = m.group(1)
                    seen_name = True
                    continue

            m = CLUSTER_IP_RE.match(line)
            if m:
                service_data["clusterIP"] = m.group(1)
                continue

            m = TYPE_RE.match(line)
            if m:
                service_data["type"] = m.group(1)
                continue

            m = NODEPORT_RE.match(line)
            if m:
                service_data["nodePorts"].append(int(m.group(1)))
                continue

        if service_data["name"] is None:
            raise ValueError("Service object without metadata.name found; malformed YAML?")

        services.append(service_data)

    return services


# ----------------------------------------------------------------------
#                         Pytest test cases
# ----------------------------------------------------------------------
def test_manifest_directory_exists():
    assert MANIFEST_DIR.exists(), (
        f"Required directory '{MANIFEST_DIR}' is missing.\n"
        "It must already exist and contain the Kubernetes manifest files."
    )
    assert MANIFEST_DIR.is_dir(), (
        f"'{MANIFEST_DIR}' exists but is not a directory."
    )


def test_expected_manifest_files_present():
    found_files = {p.name for p in MANIFEST_DIR.iterdir() if p.is_file()}
    missing = EXPECTED_FILES - found_files
    extras = found_files - EXPECTED_FILES

    assert not missing, (
        "One or more required manifest files are missing in "
        f"{MANIFEST_DIR}:\n  - " + "\n  - ".join(sorted(missing))
    )
    # Having extra files is not necessarily harmful, but we flag them
    # so the exercise author knows the starting snapshot changed.
    assert not extras, (
        "Unexpected extra file(s) found in the manifest directory:\n  - "
        + "\n  - ".join(sorted(extras))
    )


def test_manifest_contents_match_truth():
    """
    Parse every Service object from all manifest files and make sure they
    exactly match the ground-truth provided by the exercise description.
    """
    collected: Dict[str, Dict] = {}

    for file_name in EXPECTED_FILES:
        path = MANIFEST_DIR / file_name
        text = path.read_text(encoding="utf-8")
        for svc in parse_services_from_text(text):
            svc_name = svc["name"]
            assert svc_name not in collected, (
                f"Duplicate Service definition for '{svc_name}' found "
                f"in file {file_name}."
            )
            collected[svc_name] = svc

    # 1) Correct number of Services
    assert set(collected) == set(TRUTH_SERVICES), (
        "Mismatch in Service names detected.\n"
        f"Expected: {sorted(TRUTH_SERVICES)}\n"
        f"Found   : {sorted(collected)}"
    )

    # 2) Validate fields for each Service
    for name, truth in TRUTH_SERVICES.items():
        observed = collected[name]

        # 2a) ClusterIP
        assert observed["clusterIP"] == truth["clusterIP"], (
            f"Service '{name}' has unexpected clusterIP.\n"
            f"Expected: {truth['clusterIP']}\n"
            f"Found   : {observed['clusterIP']}"
        )

        # 2b) Service type
        assert observed["type"] == truth["type"], (
            f"Service '{name}' has unexpected type.\n"
            f"Expected: {truth['type']}\n"
            f"Found   : {observed['type']}"
        )

        # 2c) NodePorts
        assert sorted(observed["nodePorts"]) == sorted(truth["nodePorts"]), (
            f"Service '{name}' nodePort list differs from expectation.\n"
            f"Expected: {truth['nodePorts']}\n"
            f"Found   : {observed['nodePorts']}"
        )

        # 2d) If type is NodePort, verify range compliance
        if truth["type"] == "NodePort":
            in_range = [
                30000 <= np <= 32767 for np in truth["nodePorts"]
            ]
            # From the truth table we already know whether they should
            # all be in range or not, so we simply replicate that logic
            # and assert equality.
            expected_status = (
                "OK" if all(in_range)
                else "OUT_OF_RANGE"
            )
            observed_status = (
                "OK" if all(30000 <= np <= 32767 for np in observed["nodePorts"])
                else "OUT_OF_RANGE"
            )
            assert observed_status == expected_status, (
                f"Service '{name}' nodePort range validation failed.\n"
                f"Expected status: {expected_status}\n"
                f"Observed status: {observed_status}"
            )


def test_no_output_artifacts_exist_yet():
    """
    Ensure that the student has *not* already created output artefacts.
    This keeps the checker focussed on the 'initial state'.
    """
    output_dir = pathlib.Path("/home/user/network_diagnostics")
    assert not output_dir.exists(), (
        "The diagnostics directory '/home/user/network_diagnostics' "
        "already exists, but it should only be created by the student's "
        "solution script."
    )