# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the filesystem
# before the student writes any solution code.  It checks that the
# provided “.po” files are present, that no solution artefacts are
# present yet, and that the message/translation counts inside the
# files match the truth values described in the task.

import os
import pathlib
import re

import pytest

BASE_DIR = pathlib.Path("/home/user/project/i18n")
ES_FILE = BASE_DIR / "es.po"
FR_FILE = BASE_DIR / "fr.po"
POT_FILE = BASE_DIR / "template.pot"
SCRIPT_FILE = BASE_DIR / "generate_translation_report.sh"
LOG_FILE = BASE_DIR / "translation_report.log"


@pytest.fixture(scope="module")
def es_content():
    with ES_FILE.open(encoding="utf-8") as fh:
        return fh.readlines()


@pytest.fixture(scope="module")
def fr_content():
    with FR_FILE.open(encoding="utf-8") as fh:
        return fh.readlines()


@pytest.mark.parametrize(
    "path_to_check",
    [BASE_DIR, ES_FILE, FR_FILE, POT_FILE],
)
def test_required_paths_exist(path_to_check):
    assert path_to_check.exists(), f"Expected '{path_to_check}' to exist."


def test_solution_files_absent_initially():
    assert not SCRIPT_FILE.exists(), (
        "generate_translation_report.sh should NOT exist yet in the initial state."
    )
    assert not LOG_FILE.exists(), (
        "translation_report.log should NOT exist yet in the initial state."
    )


def _count_stats(lines):
    """
    Return (total, translated) tuple for the provided .po file lines.

    * total       – number of msgid lines *after* the header
    * translated  – number of non-empty msgstr lines *after* the header
    """
    header_finished = False
    total = 0
    translated = 0

    msgid_re = re.compile(r'^msgid\s+"(.*)"')
    msgstr_re = re.compile(r'^msgstr\s+"(.*)"')

    for line in lines:
        # Detect the end of the header by the first '#:' marker
        if not header_finished and line.startswith("#:"):
            header_finished = True

        if not header_finished:
            continue  # still inside header; ignore

        m_id = msgid_re.match(line)
        if m_id:
            total += 1
            continue

        m_str = msgstr_re.match(line)
        if m_str:
            if m_str.group(1) != "":
                translated += 1

    return total, translated


def test_es_counts(es_content):
    total, translated = _count_stats(es_content)
    assert total == 3, f"es.po should have total=3 messages, found {total}"
    assert translated == 2, (
        f"es.po should have translated=2 messages, found {translated}"
    )
    assert (total - translated) == 1, (
        f"es.po should have untranslated=1 message, "
        f"found {total - translated}"
    )


def test_fr_counts(fr_content):
    total, translated = _count_stats(fr_content)
    assert total == 3, f"fr.po should have total=3 messages, found {total}"
    assert translated == 1, (
        f"fr.po should have translated=1 message, found {translated}"
    )
    assert (total - translated) == 2, (
        f"fr.po should have untranslated=2 messages, "
        f"found {total - translated}"
    )