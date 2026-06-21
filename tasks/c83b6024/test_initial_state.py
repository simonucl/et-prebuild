# test_initial_state.py
#
# This pytest suite verifies the **initial** environment _before_ the
# student begins their work.  It checks that the original evidence files
# exist with the exact expected contents and that no response workspace
# has been created yet.

from pathlib import Path
import pytest

HOME = Path("/home/user")
LOG_DIR = HOME / "logs"

HTTP_LOG = LOG_DIR / "http-access-incident.log"
FIREWALL_LOG = LOG_DIR / "firewall-20240614.log"

INCIDENT_RESPONSE_DIR = HOME / "incident_response"


@pytest.fixture(scope="module")
def expected_http_log():
    # NB: each line ends with a trailing newline
    return (
        '192.168.1.50 - - [14/Jun/2024:02:15:23 +0000] "GET /admin/login.php HTTP/1.1" 404 560 "-" "Mozilla/5.0"\n'
        '203.0.113.77 - - [14/Jun/2024:02:16:01 +0000] "POST /wp-login.php HTTP/1.1" 200 482 "-" "Mozilla/5.0"\n'
        '198.51.100.23 - - [14/Jun/2024:02:16:22 +0000] "GET / HTTP/1.1" 200 762 "-" "curl/7.68.0"\n'
    )


@pytest.fixture(scope="module")
def expected_firewall_log():
    return (
        "Jun 14 02:15:24 host kernel: [UFW BLOCK] IN=eth0 OUT= MAC=00:0c:29:4f:8e:35 SRC=203.0.113.77 "
        "DST=192.168.1.10 LEN=60 TOS=0x00 PREC=0x00 TTL=47 ID=54321 DF PROTO=TCP SPT=55932 DPT=80 "
        "WINDOW=29200 RES=0x00 SYN URGP=0\n"
        "Jun 14 02:16:10 host kernel: [UFW BLOCK] IN=eth0 OUT= MAC=00:0c:29:4f:8e:35 SRC=198.51.100.23 "
        "DST=192.168.1.10 LEN=60 TOS=0x00 PREC=0x00 TTL=49 ID=12345 DF PROTO=TCP SPT=49000 DPT=22 "
        "WINDOW=29200 RES=0x00 SYN URGP=0\n"
    )


def test_log_directory_exists():
    assert LOG_DIR.is_dir(), f"Required directory {LOG_DIR} does not exist."


def test_original_log_files_exist():
    missing = [str(p) for p in (HTTP_LOG, FIREWALL_LOG) if not p.is_file()]
    assert not missing, f"Missing required log file(s): {', '.join(missing)}"


def test_http_log_contents(expected_http_log):
    actual = HTTP_LOG.read_text(encoding="utf-8")
    assert (
        actual == expected_http_log
    ), f"Contents of {HTTP_LOG} do not match the expected baseline."


def test_firewall_log_contents(expected_firewall_log):
    actual = FIREWALL_LOG.read_text(encoding="utf-8")
    assert (
        actual == expected_firewall_log
    ), f"Contents of {FIREWALL_LOG} do not match the expected baseline."


def test_incident_response_directory_not_present():
    assert (
        not INCIDENT_RESPONSE_DIR.exists()
    ), f"{INCIDENT_RESPONSE_DIR} should not exist before the student starts."