# test_initial_state.py
#
# This pytest suite validates the *initial* state of the operating
# system / filesystem **before** the student performs any action for the
# “restore-config” exercise.  If any test here fails, it means the
# starting snapshot is not pristine and the exercise cannot be graded
# reliably.

import os
import tarfile
from pathlib import Path

BASE_DIR = Path("/home/user/restore_test")
ARCHIVE = BASE_DIR / "backup_config.tar.gz"

TIMEZONE_INSIDE_TAR = "restore_snapshot/etc/timezone"
LOCALE_INSIDE_TAR = "restore_snapshot/etc/locale.conf"

EXPECTED_TZ_CONTENT = b"UTC\n"
EXPECTED_LOCALE_CONTENT = b"LANG=fr_FR.UTF-8\n"


def test_archive_exists_and_is_regular_file():
    """
    The compressed snapshot must be present as a *regular* file so that
    the student can unpack it.
    """
    assert ARCHIVE.exists(), (
        f"Required archive not found: {ARCHIVE} — the exercise cannot start."
    )
    assert ARCHIVE.is_file(), (
        f"{ARCHIVE} exists but is not a regular file."
    )


def test_archive_contains_expected_members_with_correct_content():
    """
    Verify that the archive contains exactly the two expected files with
    their original (pre-edited) contents.
    """
    try:
        with tarfile.open(ARCHIVE, "r:gz") as tf:
            # 1) Presence checks
            for member_name in (TIMEZONE_INSIDE_TAR, LOCALE_INSIDE_TAR):
                assert member_name in tf.getnames(), (
                    f"Archive {ARCHIVE} is missing expected member {member_name!r}."
                )
            # 2) Content checks
            tz_bytes = tf.extractfile(TIMEZONE_INSIDE_TAR).read()
            locale_bytes = tf.extractfile(LOCALE_INSIDE_TAR).read()

        assert tz_bytes == EXPECTED_TZ_CONTENT, (
            f"Unexpected initial content for {TIMEZONE_INSIDE_TAR!r} inside the archive.\n"
            f"Expected: {EXPECTED_TZ_CONTENT!r}\nFound:    {tz_bytes!r}"
        )
        assert locale_bytes == EXPECTED_LOCALE_CONTENT, (
            f"Unexpected initial content for {LOCALE_INSIDE_TAR!r} inside the archive.\n"
            f"Expected: {EXPECTED_LOCALE_CONTENT!r}\nFound:    {locale_bytes!r}"
        )
    except tarfile.ReadError as exc:
        assert False, f"Cannot open {ARCHIVE}: {exc}"


def test_restore_snapshot_not_yet_unpacked():
    """
    Before the student starts, *nothing* should have been unpacked.
    The directory restore_snapshot/ should therefore not exist at all.
    """
    extracted_dir = BASE_DIR / "restore_snapshot"
    assert not extracted_dir.exists(), (
        f"Directory {extracted_dir} already exists — the archive appears to have "
        f"been unpacked prematurely.  Start with a clean state."
    )


def test_validation_log_absent():
    """
    The validation log must not pre-exist; it should be created by the
    student during the exercise.
    """
    validation_log = BASE_DIR / "validation.log"
    assert not validation_log.exists(), (
        f"{validation_log} unexpectedly already exists — the initial state "
        f"must not include the validation log."
    )