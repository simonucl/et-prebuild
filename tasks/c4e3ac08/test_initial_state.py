# test_initial_state.py
"""
Pytest suite that verifies the container's **initial** state *before* the learner
attempts the exercise.

We only test immutable, environment-wide facts that must already be true and
must stay true throughout the challenge:

1. The system’s primary time-zone identifier must be “Etc/UTC”.
2. The system’s primary locale identifier must be “C.UTF-8”.

Per the authoring guidelines we deliberately do **not** look at (or for) any of
the task’s output artefacts such as /home/user/logs or
/home/user/logs/system_context.log.
"""

import os
import locale
import time
import pathlib

import pytest


def _detect_timezone() -> str:
    """
    Try a few different (portable) mechanisms to discover the canonical
    time-zone identifier of the running container.

    Preference order:
    1. /etc/timezone       (common on Debian/Ubuntu)
    2. /etc/localtime symlink into /usr/share/zoneinfo
    3. Python’s time.tzname (last-ditch fallback; may be less specific)

    Returns
    -------
    str
        The best-effort time-zone identifier (e.g. "Etc/UTC", "Europe/Berlin").
    """
    # 1. /etc/timezone (text file containing the tz string)
    tz_file = pathlib.Path("/etc/timezone")
    if tz_file.is_file():
        tz = tz_file.read_text().strip()
        if tz:
            return tz

    # 2. /etc/localtime -> /usr/share/zoneinfo/<Region>/<City>
    localtime = pathlib.Path("/etc/localtime")
    if localtime.exists():
        realpath = localtime.resolve()
        try:
            # Ensure we only strip the prefix if it is actually part of the path
            zoneinfo_prefix = pathlib.Path("/usr/share/zoneinfo")
            tz = realpath.relative_to(zoneinfo_prefix)
            return str(tz)
        except ValueError:
            # /etc/localtime is not inside /usr/share/zoneinfo; fall through
            pass

    # 3. Fallback: Python's perception of the TZ name
    # time.tzname is a tuple (std, dst). We use the first entry.
    return time.tzname[0]


def _detect_locale() -> str:
    """
    Obtain the current locale in a reliable way without changing it.

    locale.setlocale(category) without the second argument returns the current
    setting for that category as a string.
    """
    return locale.setlocale(locale.LC_CTYPE)


def test_system_timezone_is_etc_utc():
    """
    The grading container is expected to run in the Etc/UTC time-zone.
    """
    detected = _detect_timezone()
    assert (
        detected == "Etc/UTC"
    ), (
        "The container's time-zone must be 'Etc/UTC' "
        f"(detected: {detected!r}). "
        "Please contact the course staff if this assertion fails, "
        "because the challenge relies on that specific setting."
    )


def test_system_locale_is_c_utf8():
    """
    The grading container is expected to use the C.UTF-8 locale.
    """
    detected = _detect_locale()
    assert (
        detected == "C.UTF-8"
    ), (
        "The container's locale must be 'C.UTF-8' "
        f"(detected: {detected!r}). "
        "Please contact the course staff if this assertion fails, "
        "because the challenge relies on that specific setting."
    )