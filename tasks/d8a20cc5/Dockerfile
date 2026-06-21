FROM ubuntu:22.04

# ------------------------------------------------------------------
# Install required OS packages
# ------------------------------------------------------------------
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip sqlite3 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Pip packages
RUN pip3 install --no-cache-dir pytest

# Provide a convenient `python` alias
RUN ln -sf /usr/bin/python3 /usr/bin/python

# ------------------------------------------------------------------
# Prepare initial filesystem state for the exercise
# ------------------------------------------------------------------
# Home directory for the learner
RUN mkdir -p /home/user && \
    chmod 777 /home/user

# Releases directory with correct permissions
RUN mkdir -p /home/user/releases && \
    chmod 755 /home/user/releases

# ------------------------------------------------------------------
# Create the SQLite database with the required schema and data
# ------------------------------------------------------------------
RUN sqlite3 /home/user/releases/app_releases.db <<'SQL'
CREATE TABLE releases (
        version TEXT PRIMARY KEY,
        status  TEXT NOT NULL
);
INSERT INTO releases (version, status) VALUES
('v1.0.0','released'),
('v1.1.0','released'),
('v2.0.0','released'),
('v2.1.0-beta','pending'),
('v2.2.0','pending');
SQL

# Ensure world-readable permissions; no write needed for learners
RUN chmod 644 /home/user/releases/app_releases.db

# Keep PATH sane; do not override HOME
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

WORKDIR /home/user