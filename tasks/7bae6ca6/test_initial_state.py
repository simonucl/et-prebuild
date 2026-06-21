# test_initial_state.py
"""
Pytest suite that validates the operating-system / filesystem state
BEFORE the student runs any solution code for the task
“Filter Research Upload Logs with a Single Regex Command”.

We confirm that:
1. The source log exists with the exact expected contents.
2. The destination directory and file do NOT yet exist.
"""

import os
from pathlib import Path

ACCESS_LOG = Path("/home/user/datasets/access.log")
FILTERED_DIR = Path("/home/user/datasets/filtered")
DEST_FILE = FILTERED_DIR / "climate_uploads_201.log"

EXPECTED_ACCESS_LOG_CONTENT = (
    "[2024-03-01 10:15:00] DATASET:climate_arctic_ice UPLOADED BY alice STATUS 201 TIME 456\n"
    "[2024-03-01 10:17:42] DATASET:geology_rock_layers UPLOADED BY bob STATUS 201 TIME 512\n"
    "[2024-03-02 09:03:11] DATASET:climate_global_temp UPLOADED BY carol STATUS 500 TIME 789\n"
    "[2024-03-02 11:45:33] DATASET:climate_atmos_CO2 UPLOADED BY dave STATUS 201 TIME 300\n"
    "[2024-03-02 12:00:00] DATASET:biology_cell_images UPLOADED BY eve STATUS 201 TIME 102\n"
    "[2024-03-03 08:20:20] DATASET:climate_ocean_salinity UPLOADED BY frank STATUS 201 TIME 402\n"
    "[2024-03-03 09:10:05] DATASET:climate_arctic_ice UPLOADED BY alice STATUS 404 TIME 150\n"
    "[2024-03-03 10:11:11] DATASET:physics_particle_tracks UPLOADED BY grace STATUS 201 TIME 250\n"
)

def test_access_log_exists_and_is_file():
    assert ACCESS_LOG.exists(), f"Expected source log at {ACCESS_LOG} does not exist."
    assert ACCESS_LOG.is_file(), f"The path {ACCESS_LOG} exists but is not a regular file."

def test_access_log_contents_are_as_expected():
    actual = ACCESS_LOG.read_text(encoding="utf-8")
    assert actual == EXPECTED_ACCESS_LOG_CONTENT, (
        "The contents of /home/user/datasets/access.log are not as expected.\n"
        "If this file has been modified or corrupted, restore it to the original state "
        "before attempting the task."
    )

def test_filtered_directory_does_not_exist_yet():
    assert not FILTERED_DIR.exists(), (
        f"The directory {FILTERED_DIR} should NOT exist before the task begins."
    )

def test_destination_file_does_not_exist_yet():
    assert not DEST_FILE.exists(), (
        f"The destination file {DEST_FILE} should NOT exist before the task begins."
    )