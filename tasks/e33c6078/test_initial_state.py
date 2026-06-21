# test_initial_state.py
"""
Pytest suite that verifies the *initial* state of the operating system /
filesystem before the student begins working on the capacity-planning task.

DO NOT modify this file.
"""

import configparser
import re
from pathlib import Path

DATA_DIR = Path("/home/user/capacity_planner/data")
SUMMARY_DIR = Path("/home/user/capacity_planner/summary")
RISK_LOG = SUMMARY_DIR / "capacity_risk_2024-08.log"
MARKER_FILE = SUMMARY_DIR / "analysis.done"

# Regex for an ISO-8601 calendar date (YYYY-MM-DD)
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}$")


def test_data_directory_exists():
    assert DATA_DIR.exists(), f"Required directory {DATA_DIR} is missing."
    assert DATA_DIR.is_dir(), f"{DATA_DIR} exists but is not a directory."


def _iter_ini_files():
    """Yield all *.ini files inside the data directory."""
    for path in sorted(DATA_DIR.glob("*.ini")):
        if path.is_file():
            yield path


def test_expected_ini_files_present():
    """
    The starter repository must contain at least the three known sample files.
    Extra files are allowed but these three are mandatory.
    """
    expected = {f"server{n:02d}.ini" for n in (1, 2, 3)}
    found = {p.name for p in _iter_ini_files()}
    missing = expected - found
    assert not missing, (
        "The following required INI files are missing from "
        f"{DATA_DIR}: {', '.join(sorted(missing))}"
    )


def _parse_ini(path: Path) -> configparser.ConfigParser:
    """Read an INI file while preserving key case."""
    cp = configparser.ConfigParser(interpolation=None)
    cp.optionxform = str  # preserve key case sensitivity
    with path.open() as fh:
        cp.read_file(fh)
    return cp


def test_ini_file_structure():
    """
    Every INI file must satisfy:

    • Exactly three sections whose names are ISO-8601 dates.
    • Each section contains exactly the keys: CPU, Memory, Disk.
    • All values must be valid integers.
    """
    for ini_path in _iter_ini_files():
        cp = _parse_ini(ini_path)

        # --- Section checks -------------------------------------------------
        sections = cp.sections()
        assert len(sections) == 3, (
            f"{ini_path}: expected exactly 3 sections, got {len(sections)} "
            f"({sections})"
        )

        for section in sections:
            assert DATE_RE.fullmatch(section), (
                f"{ini_path}: section '{section}' is not a valid ISO-8601 date."
            )

            # --- Key checks --------------------------------------------------
            keys = cp[section].keys()
            expected_keys = {"CPU", "Memory", "Disk"}
            assert set(keys) == expected_keys, (
                f"{ini_path} / [{section}]: expected keys "
                f"{sorted(expected_keys)}, got {sorted(keys)}"
            )

            # --- Value checks ------------------------------------------------
            for key, value in cp[section].items():
                try:
                    int(value)
                except ValueError as e:
                    raise AssertionError(
                        f"{ini_path} / [{section}] {key}= '{value}' "
                        "is not a valid integer."
                    ) from e


def test_output_files_do_not_exist_yet():
    """
    The summary artefacts must *not* be present before the student runs their
    solution script.  Their existence would indicate that the task was run
    prematurely or that stale data is on disk.
    """
    assert not RISK_LOG.exists(), (
        f"Output file {RISK_LOG} already exists before the task starts. "
        "Remove it so tests can verify fresh creation."
    )
    assert not MARKER_FILE.exists(), (
        f"Marker file {MARKER_FILE} already exists before the task starts. "
        "Remove it so tests can verify fresh creation."
    )