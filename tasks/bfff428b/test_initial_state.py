# test_initial_state.py
"""
Pytest suite that validates the *initial* operating-system / filesystem
state *before* the student performs any action.

The suite deliberately avoids looking for – or complaining about – any of
the files or directories that the student is supposed to create later on.
Only the pre-supplied Nmap XML scan is inspected.

Stdlib-only (plus pytest) as required.
"""

import os
import stat
import xml.etree.ElementTree as ET
import pytest

# --------------------------------------------------------------------------- #
# Constants                                                                   #
# --------------------------------------------------------------------------- #
XML_PATH = "/home/user/raw_scans/nmap_scan1.xml"

# These are the lines that should be produced *from* the XML; they are used
# here solely to verify that the XML contains what the assignment describes.
EXPECTED_LINES = [
    "HOST 192.168.1.10 PORT 22/tcp SERVICE ssh",
    "HOST 192.168.1.10 PORT 80/tcp SERVICE http",
    "HOST 192.168.1.11 PORT 21/tcp SERVICE ftp",
    "HOST 192.168.1.11 PORT 139/tcp SERVICE netbios-ssn",
    "HOST 192.168.1.11 PORT 445/tcp SERVICE microsoft-ds",
]


# --------------------------------------------------------------------------- #
# Helper functions                                                            #
# --------------------------------------------------------------------------- #
def sort_key(summary_line: str):
    """
    Sorting helper:
    Splits "HOST <ip> PORT <port>/tcp SERVICE <svc>" into a sortable key
    of (ipOctet1, ipOctet2, ipOctet3, ipOctet4, port).
    """
    parts = summary_line.split()
    ip_str = parts[1]
    port_str = parts[3].split("/")[0]
    return tuple(int(octet) for octet in ip_str.split(".")) + (int(port_str),)


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #
def test_raw_scans_directory_exists():
    """Ensure the /home/user/raw_scans directory is present."""
    dir_path = os.path.dirname(XML_PATH)
    assert os.path.isdir(dir_path), (
        f"Required directory '{dir_path}' is missing.\n"
        "It must exist and contain the pre-supplied Nmap XML scan."
    )


def test_nmap_scan_file_exists_and_permissions():
    """The XML file must exist and be world-readable (0644)."""
    assert os.path.isfile(XML_PATH), (
        f"Expected XML scan file '{XML_PATH}' is missing."
    )

    mode = os.stat(XML_PATH).st_mode & 0o777
    assert mode == 0o644, (
        f"File '{XML_PATH}' should have permissions 0644 "
        f"but currently has {oct(mode)}."
    )


def test_nmap_scan_contents_match_expected():
    """
    Parse the XML and verify that it contains exactly the open TCP ports
    described in the task statement.  This guarantees that the student
    starts with the correct, unmodified scan data.
    """
    try:
        root = ET.parse(XML_PATH).getroot()
    except ET.ParseError as exc:
        pytest.fail(f"Unable to parse '{XML_PATH}' as XML: {exc}")

    assert root.tag == "nmaprun", (
        f"Unexpected root element '{root.tag}' in '{XML_PATH}'. "
        "Expected 'nmaprun'."
    )

    # Collect summary lines using the same rules the student must apply.
    extracted_lines = []
    for host in root.findall("host"):
        status_el = host.find("status")
        if status_el is None or status_el.get("state") != "up":
            continue

        addr_el = host.find("address")
        if addr_el is None:
            continue
        ip = addr_el.get("addr")

        for port_el in host.findall("./ports/port"):
            if port_el.get("protocol") != "tcp":
                continue
            state_el = port_el.find("state")
            if state_el is None or state_el.get("state") != "open":
                continue
            portid = port_el.get("portid")
            service_el = port_el.find("service")
            service_name = service_el.get("name") if service_el is not None else ""

            extracted_lines.append(
                f"HOST {ip} PORT {portid}/tcp SERVICE {service_name}"
            )

    extracted_lines = sorted(extracted_lines, key=sort_key)

    assert extracted_lines == EXPECTED_LINES, (
        "The pre-supplied Nmap XML does not contain the expected set of "
        "open TCP ports.\n"
        "EXPECTED:\n  " + "\n  ".join(EXPECTED_LINES) + "\n\n"
        "FOUND:\n  " + ("\n  ".join(extracted_lines) if extracted_lines else "(none)")
    )