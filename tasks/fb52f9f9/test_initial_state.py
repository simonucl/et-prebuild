# test_initial_state.py
#
# This pytest suite verifies the initial, pre-exercise state of the
# filesystem for the “re-scrape the HTML table” task.  It checks only
# for the existence and correctness of the PROVIDED input artefacts
# and intentionally avoids touching any output paths.

import os
import re
from pathlib import Path

INPUT_HTML = Path("/home/user/projects/scrape/input/page.html")


def test_input_file_exists_and_is_readable():
    """
    The captured HTML page must already be present before the student
    starts the exercise.  It must be a regular, readable file.
    """
    assert INPUT_HTML.exists(), (
        f"Missing required input file: {INPUT_HTML} – it must already be "
        "present for the exercise to make sense."
    )
    assert INPUT_HTML.is_file(), (
        f"Expected {INPUT_HTML} to be a regular file, but something else "
        "was found (e.g. directory, symlink)."
    )
    # Basic readability check
    try:
        INPUT_HTML.read_text(encoding="utf-8")
    except Exception as exc:  # pylint: disable=broad-except
        raise AssertionError(
            f"Could not read {INPUT_HTML} as UTF-8: {exc}"
        ) from exc


def test_sales_table_presence_and_headers():
    """
    The HTML must contain exactly one table with id="sales" and the
    expected column headers.  This confirms that the student receives
    the correct raw data to work with.
    """
    content = INPUT_HTML.read_text(encoding="utf-8")

    # 1) The table with id="sales" must exist.
    table_re = re.compile(
        r"<table\b[^>]*\bid\s*=\s*[\"']sales[\"'][^>]*>",
        re.IGNORECASE | re.DOTALL,
    )
    assert table_re.search(content), (
        "The input HTML does not contain a <table> element with id='sales'. "
        "Verify that the file is unmodified and correctly captured."
    )

    # 2) Column headers must be present somewhere in the table.
    for header in ("Region", "Sales", "Quarter"):
        assert header in content, (
            f"The header '{header}' is missing from the sales table in "
            f"{INPUT_HTML}.  The table structure should remain intact."
        )