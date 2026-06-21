# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the operating system /
# filesystem for the “translations” exercise.
#
# NOTE:
# • This file intentionally does NOT check for the presence of the output file
#   “/home/user/translations/translation_report.log”.
# • Only the existing source material is verified.

import pathlib
import pytest

TRANSLATIONS_DIR = pathlib.Path("/home/user/translations")

# Expected ground-truth values (taken from the task description)
EXPECTED = {
    "TOTAL_FILES": 3,
    "TOTAL_MSGID": 15,
    "TOTAL_UNTRANSLATED": 4,
    "EN_TRANSLATED": 5,
    "ES_TRANSLATED": 4,
    "FR_TRANSLATED": 2,
}

PO_FILES = {
    "en": TRANSLATIONS_DIR / "en.po",
    "es": TRANSLATIONS_DIR / "es.po",
    "fr": TRANSLATIONS_DIR / "fr.po",
}


def _po_stats(po_path: pathlib.Path):
    """
    Return a tuple with three integers for a single .po file:

        (msgid_count, untranslated_count, translated_count)
    """
    msgid_count = 0
    untranslated_count = 0
    translated_count = 0

    with po_path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line.startswith("msgid "):
                msgid_count += 1
            elif line.startswith('msgstr "'):
                if line == 'msgstr ""':
                    untranslated_count += 1
                else:
                    translated_count += 1

    return msgid_count, untranslated_count, translated_count


def test_translations_directory_exists():
    assert TRANSLATIONS_DIR.is_dir(), (
        f"Required directory {TRANSLATIONS_DIR} is missing. "
        "It must exist *before* you generate the report."
    )


@pytest.mark.parametrize("lang", PO_FILES.keys())
def test_po_file_exists(lang):
    po_path = PO_FILES[lang]
    assert po_path.is_file(), (
        f"Expected .po file for language '{lang}' not found at {po_path}."
    )
    # Basic sanity: ensure file is not empty
    assert po_path.stat().st_size > 0, f"{po_path} appears to be empty."


def test_po_file_counts_are_as_expected():
    total_files = len([p for p in TRANSLATIONS_DIR.glob("*.po") if p.is_file()])
    assert (
        total_files == EXPECTED["TOTAL_FILES"]
    ), f"Expected {EXPECTED['TOTAL_FILES']} .po files, found {total_files}."

    grand_msgid = grand_untranslated = 0
    per_file_translated = {}

    for lang, po_path in PO_FILES.items():
        msgid_cnt, untranslated_cnt, translated_cnt = _po_stats(po_path)
        grand_msgid += msgid_cnt
        grand_untranslated += untranslated_cnt
        per_file_translated[lang.upper()] = translated_cnt

    assert (
        grand_msgid == EXPECTED["TOTAL_MSGID"]
    ), f"Expected TOTAL_MSGID={EXPECTED['TOTAL_MSGID']}, got {grand_msgid}."

    assert (
        grand_untranslated == EXPECTED["TOTAL_UNTRANSLATED"]
    ), (
        f"Expected TOTAL_UNTRANSLATED={EXPECTED['TOTAL_UNTRANSLATED']}, "
        f"got {grand_untranslated}."
    )

    for lang_key, expected_val in (
        ("EN", EXPECTED["EN_TRANSLATED"]),
        ("ES", EXPECTED["ES_TRANSLATED"]),
        ("FR", EXPECTED["FR_TRANSLATED"]),
    ):
        assert (
            per_file_translated[lang_key] == expected_val
        ), (
            f"Expected {lang_key}_TRANSLATED={expected_val}, "
            f"got {per_file_translated[lang_key]}."
        )