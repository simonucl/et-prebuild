# test_initial_state.py
#
# This pytest suite verifies that the **initial** filesystem state—
# the one that is present *before* the student executes any code—
# contains the required fixture HTML pages exactly as described in
# the task.  It intentionally makes **no reference** to any output
# paths such as /home/user/scrape_output/.*

import pathlib
import textwrap

import pytest

# Base directory that must already exist
PAGES_DIR = pathlib.Path("/home/user/iot_dashboard/pages")

# Mapping of expected filenames → their exact, one-line HTML content
EXPECTED_FILES = {
    "device_001.html": (
        "<html><body><span id=\"device-id\">001</span><span id=\"temp\">23.7</span>"
        "<span id=\"hum\">50</span><span id=\"bat\">87</span>"
        "<span id=\"ts\">2024-03-11T15:04:22Z</span></body></html>"
    ),
    "device_002.html": (
        "<html><body><span id=\"device-id\">002</span><span id=\"temp\">21.9</span>"
        "<span id=\"hum\">49</span><span id=\"bat\">92</span>"
        "<span id=\"ts\">2024-03-11T15:04:34Z</span></body></html>"
    ),
    "device_003.html": (
        "<html><body><span id=\"device-id\">003</span><span id=\"temp\">24.5</span>"
        "<span id=\"hum\">48</span><span id=\"bat\">90</span>"
        "<span id=\"ts\">2024-03-11T15:04:47Z</span></body></html>"
    ),
}


def _read_single_line(path: pathlib.Path) -> str:
    """
    Read the file and return its **single** line without the trailing newline.
    If the file contains more than one physical line, raise an assertion.
    """
    text = path.read_text(encoding="utf-8")
    # It is supposed to be exactly one physical line without surrounding spaces.
    lines = text.splitlines()
    assert (
        len(lines) == 1
    ), f"{path} should contain exactly one line, found {len(lines)} lines."
    return lines[0]


def test_pages_directory_exists():
    """The base directory containing the HTML pages must exist and be a directory."""
    assert PAGES_DIR.exists(), f"Required directory {PAGES_DIR} is missing."
    assert PAGES_DIR.is_dir(), f"{PAGES_DIR} exists but is not a directory."


@pytest.mark.parametrize("filename,expected_content", EXPECTED_FILES.items())
def test_each_expected_html_file_exists_and_is_correct(filename, expected_content):
    """
    For each expected HTML fixture:
    1. Verify that the file exists.
    2. Verify it is a regular file (not a dir or symlink).
    3. Verify its contents exactly match the specification.
    """
    file_path = PAGES_DIR / filename
    assert file_path.exists(), f"Required file {file_path} is missing."
    assert file_path.is_file(), f"{file_path} exists but is not a regular file."

    actual_content = _read_single_line(file_path)
    assert (
        actual_content == expected_content
    ), textwrap.dedent(
        f"""\
        Content mismatch in {file_path}.
        Expected:
        {expected_content!r}
        Found:
        {actual_content!r}
        """
    )


def test_glob_matches_at_least_expected_files():
    """
    The student will glob for /home/user/iot_dashboard/pages/device_*.html.
    Ensure that all expected fixture files are present in that glob.
    Additional files are allowed but these three are mandatory.
    """
    globbed = {p.name for p in PAGES_DIR.glob("device_*.html")}
    missing = set(EXPECTED_FILES) - globbed
    assert not missing, (
        "The following expected files are missing from the glob pattern "
        f"device_*.html: {', '.join(sorted(missing))}"
    )