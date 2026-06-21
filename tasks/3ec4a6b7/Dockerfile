FROM ubuntu:22.04

RUN set -e && \
    echo "Updating package index and installing Python tooling..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    echo "Creating required directory structure and slow query log..." && \
    mkdir -p /home/user/db/logs && \
    chmod 755 /home/user /home/user/db /home/user/db/logs

RUN cat > /home/user/db/logs/slow_queries.log << 'EOF'
SELECT * FROM users WHERE id = ?;
SELECT * FROM users WHERE id = ?;
SELECT * FROM users WHERE id = ?;
SELECT * FROM orders WHERE status = 'pending';
SELECT * FROM orders WHERE status = 'pending';
UPDATE users SET last_login = NOW() WHERE id = ?;
DELETE FROM sessions WHERE user_id = ?;
DELETE FROM sessions WHERE user_id = ?;
DELETE FROM sessions WHERE user_id = ?;
DELETE FROM sessions WHERE user_id = ?;
EOF

RUN chmod 644 /home/user/db/logs/slow_queries.log

RUN echo "Adding pytest initial-state tests..." && \
    true

RUN cat > /test_initial_state.py << 'PYEOF'
import os
from pathlib import Path
import pytest

HOME = Path("/home/user")
DB_DIR = HOME / "db"
LOG_DIR = DB_DIR / "logs"
SLOW_LOG = LOG_DIR / "slow_queries.log"

EXPECTED_LOG_LINES = [
    "SELECT * FROM users WHERE id = ?;\n",
    "SELECT * FROM users WHERE id = ?;\n",
    "SELECT * FROM users WHERE id = ?;\n",
    "SELECT * FROM orders WHERE status = 'pending';\n",
    "SELECT * FROM orders WHERE status = 'pending';\n",
    "UPDATE users SET last_login = NOW() WHERE id = ?;\n",
    "DELETE FROM sessions WHERE user_id = ?;\n",
    "DELETE FROM sessions WHERE user_id = ?;\n",
    "DELETE FROM sessions WHERE user_id = ?;\n",
    "DELETE FROM sessions WHERE user_id = ?;\n",
]

def test_log_directory_exists():
    assert LOG_DIR.exists(), f"Required directory {LOG_DIR} is missing."
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."

def test_slow_log_file_exists_and_is_file():
    assert SLOW_LOG.exists(), f"Required log file {SLOW_LOG} is missing."
    assert SLOW_LOG.is_file(), f"{SLOW_LOG} exists but is not a regular file."

def test_slow_log_contents_are_exact():
    with SLOW_LOG.open("rb") as fp:
        data = fp.read()

    assert b"\r" not in data, f"{SLOW_LOG} contains CR (\\r) characters."

    actual_lines = data.decode("utf-8").splitlines(keepends=True)

    assert actual_lines == EXPECTED_LOG_LINES, (
        "The contents of slow_queries.log differ from the expected initial state."
    )
PYEOF

RUN chmod 644 /test_initial_state.py && echo "Container setup complete."

# Author Slow-SQL-Setup