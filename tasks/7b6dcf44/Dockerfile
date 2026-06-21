# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ---------------------------------------------------------------------
# Install required system packages
# ---------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# ---------------------------------------------------------------------
# Install Python testing framework
# ---------------------------------------------------------------------
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# ---------------------------------------------------------------------
# Create filesystem layout expected by the tests
# ---------------------------------------------------------------------
RUN mkdir -p /home/user/data && \
    chmod 0755 /home/user && \
    chmod 0700 /home/user/data

# ---------------------------------------------------------------------
# Create and populate the SQLite database
# ---------------------------------------------------------------------
RUN sqlite3 /home/user/data/infra.db <<'SQL'
CREATE TABLE alerts(
    id       INTEGER PRIMARY KEY,
    severity TEXT NOT NULL,
    status   TEXT NOT NULL
);

INSERT INTO alerts (id, severity, status) VALUES
    (1, 'Sev1', 'Open'),
    (2, 'Sev1', 'Acknowledged'),
    (3, 'Sev1', 'Resolved'),
    (4, 'Sev2', 'Open'),
    (5, 'Sev1', 'Open'),
    (6, 'Sev3', 'Closed');
SQL

# Correct permissions for the DB file
RUN chmod 0644 /home/user/data/infra.db

# ---------------------------------------------------------------------
# Environment variables
# ---------------------------------------------------------------------
ENV LC_ALL=C
ENV LANG=C

# Ensure permissions at runtime as expected
RUN chmod 0755 /home/user

# ---------------------------------------------------------------------
# Default command (equivalent to %runscript)
# ---------------------------------------------------------------------
CMD ["/bin/bash"]