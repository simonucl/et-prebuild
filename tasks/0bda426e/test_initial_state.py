# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem / operating-system
# state that must be present **before** the student starts working on the
# assignment “Generate a consolidated vulnerability report from provided
# Nmap XML data”.
#
# Only pre-existing assets are checked (scan data and mapping files).  We do
# NOT test for the presence of any output files or directories that the
# student is expected to create later (e.g. /home/user/vuln_scan or the CSV /
# log files inside it).
#
# Requirements verified:
#   • /home/user/scan_data exists.
#   • /home/user/scan_data/initial_scan.xml exists and is a well-formed XML
#     file that contains exactly 5 <port> elements whose <state> is “open”,
#     each having both “product” and “version” service attributes.
#   • /home/user/scan_data/cve_mapping.csv exists, has the correct header
#     row, and contains a one-to-one mapping for every (service,version)
#     combination found in the XML.
#
# Failures raise clear, instructive messages so that any missing or malformed
# prerequisite data can be fixed before grading begins.

import os
import csv
import xml.etree.ElementTree as ET
import pytest

SCAN_DIR = "/home/user/scan_data"
XML_FILE = os.path.join(SCAN_DIR, "initial_scan.xml")
CSV_FILE = os.path.join(SCAN_DIR, "cve_mapping.csv")


@pytest.fixture(scope="module")
def xml_tree():
    """Parse the XML once for reuse in multiple tests."""
    try:
        tree = ET.parse(XML_FILE)
    except ET.ParseError as exc:
        pytest.fail(f"{XML_FILE} is not a well-formed XML file: {exc}")
    return tree


def test_scan_data_directory_exists():
    assert os.path.isdir(
        SCAN_DIR
    ), f"Expected directory {SCAN_DIR} is missing. The raw scan data must be located here."


def test_initial_scan_xml_exists_and_well_formed(xml_tree):
    # The fixture will already have failed if the XML is missing or malformed.
    assert os.path.isfile(
        XML_FILE
    ), f"Expected XML file {XML_FILE} is missing."


def test_initial_scan_xml_has_expected_open_ports(xml_tree):
    root = xml_tree.getroot()

    open_ports = []
    for host in root.findall("host"):
        addr_elem = host.find('address[@addrtype="ipv4"]')
        ip = addr_elem.get("addr") if addr_elem is not None else None

        for port in host.findall("ports/port"):
            state_elem = port.find('state[@state="open"]')
            if state_elem is None:
                continue  # only interested in open ports

            service_elem = port.find("service")
            product = service_elem.get("product") if service_elem is not None else None
            version = service_elem.get("version") if service_elem is not None else None

            assert (
                ip is not None
            ), "An <address addrtype='ipv4'> element with a valid IP is required for each host."
            assert (
                product is not None
            ), "Each open <port> must have a <service> element with a 'product' attribute."
            assert (
                version is not None
            ), "Each open <port> must have a <service> element with a 'version' attribute."

            open_ports.append((ip, port.get("portid"), port.get("protocol"), product, version))

    # The reference data contains exactly 5 open ports.
    assert (
        len(open_ports) == 5
    ), f"Expected 5 open ports in {XML_FILE}, found {len(open_ports)}."


@pytest.fixture(scope="module")
def csv_rows():
    """Read the CSV once for reuse."""
    assert os.path.isfile(
        CSV_FILE
    ), f"Expected CSV mapping file {CSV_FILE} is missing."

    with open(CSV_FILE, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)

    # Validate header columns
    expected_fields = ["service", "version", "cve_reference"]
    assert reader.fieldnames == expected_fields, (
        f"{CSV_FILE} header row must be exactly "
        f"{','.join(expected_fields)}, found: {reader.fieldnames}"
    )

    assert rows, f"{CSV_FILE} must contain at least one data row."
    return rows


def test_cve_mapping_covers_all_xml_services(xml_tree, csv_rows):
    # Build a set of (service,version) combos from the CSV for fast look-up
    csv_map = {(row["service"], row["version"]) for row in csv_rows}

    # Extract combos from XML
    xml_combos = set()
    for service_elem in xml_tree.findall(".//port/state[@state='open']/../service"):
        product = service_elem.get("product")
        version = service_elem.get("version")
        xml_combos.add((product, version))

    # There should be a one-to-one mapping
    missing = xml_combos - csv_map
    assert (
        not missing
    ), f"The following (service,version) combos are missing from {CSV_FILE}: {missing}"