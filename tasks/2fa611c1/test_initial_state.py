# test_initial_state.py
"""
Pytest suite that validates the **initial** file-system state for the
localisation‐update task *before* the student runs any commands.

Rules checked:
1. /home/user/project/i18n/messages.po must already exist.
2. The PO file must contain the four expected msgid entries:
   "File", "Edit", "View", "Help"  – in that order.
3. The corresponding msgstr lines must be:
      • empty ("") for File, Edit, Help
      • non-empty for View (specifically "Vista")
4. The file must **not** yet contain the marker "<NEEDS_TRANSLATION>".
5. Output artefacts must **not** exist yet:
      • /home/user/project/i18n/untranslated.txt
      • /home/user/update_summary.log
"""

import re
from pathlib import Path

import pytest


PO_PATH = Path("/home/user/project/i18n/messages.po")
UNTRANSLATED_PATH = Path("/home/user/project/i18n/untranslated.txt")
SUMMARY_LOG_PATH = Path("/home/user/update_summary.log")


@pytest.fixture(scope="module")
def po_lines():
    """
    Return the contents of the PO file as a list of stripped lines.
    Fail fast if the file is missing.
    """
    assert PO_PATH.is_file(), (
        f"Expected PO file at {PO_PATH} to exist, but it is missing."
    )
    with PO_PATH.open(encoding="utf-8") as fh:
        return [ln.rstrip("\n") for ln in fh]


def test_msgids_present_and_in_order(po_lines):
    """
    Verify that the user-facing msgid entries are present *exactly once*
    and in the required order: File, Edit, View, Help.
    """
    wanted_order = ["File", "Edit", "View", "Help"]
    pattern = re.compile(r'^msgid\s+"(.+)"$')

    extracted = [
        m.group(1)
        for line in po_lines
        if (m := pattern.match(line)) and m.group(1)  # ignore header msgid ""
    ]

    assert extracted == wanted_order, (
        "The PO file should contain msgid entries exactly in this order:\n"
        "  File, Edit, View, Help\n"
        f"Found instead: {extracted}"
    )


def _collect_msgstrs(po_lines):
    """
    Walk through the file and pair each msgid with its immediate msgstr.
    Returns a list of (msgid, msgstr) tuples, skipping the header entry.
    """
    pairs = []
    msgid_pattern = re.compile(r'^msgid\s+"(.+)"$')
    msgstr_pattern = re.compile(r'^msgstr\s+"(.*)"$')

    current_id = None
    for line in po_lines:
        if m := msgid_pattern.match(line):
            # Skip the header msgid ""
            current_id = m.group(1) or None
            continue
        if current_id is None:
            continue

        if m := msgstr_pattern.match(line):
            pairs.append((current_id, m.group(1)))
            current_id = None  # reset for next pair

    return pairs


def test_msgstr_values_are_correct(po_lines):
    """
    Ensure that msgstr values are empty for File, Edit, Help
    and 'Vista' for View.
    """
    expected = {
        "File": "",
        "Edit": "",
        "View": "Vista",
        "Help": "",
    }

    pairs = dict(_collect_msgstrs(po_lines))
    missing = set(expected) - set(pairs)
    assert not missing, f"Missing msgid entries in PO file: {sorted(missing)}"

    incorrect = {
        k: (pairs[k], v) for k, v in expected.items() if pairs[k] != v
    }
    assert not incorrect, (
        "Unexpected msgstr values:\n"
        + "\n".join(
            f"  {k!r}: expected {exp!r}, found {found!r}"
            for k, (found, exp) in incorrect.items()
        )
    )


def test_no_needs_translation_marker_yet(po_lines):
    """
    The marker '<NEEDS_TRANSLATION>' must NOT be present before the task runs.
    """
    marker = "<NEEDS_TRANSLATION>"
    assert marker not in "\n".join(po_lines), (
        f"The marker {marker!r} should not be present yet in {PO_PATH}."
    )


def test_output_files_do_not_exist_yet():
    """
    The task output artefacts must not exist before the student runs their
    solution.
    """
    assert not UNTRANSLATED_PATH.exists(), (
        f"Output file {UNTRANSLATED_PATH} should not exist yet."
    )
    assert not SUMMARY_LOG_PATH.exists(), (
        f"Output file {SUMMARY_LOG_PATH} should not exist yet."
    )