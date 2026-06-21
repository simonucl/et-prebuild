# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Update package lists and install required system packages
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        sqlite3 \
        python3 \
        python3-pip

# Install pytest via pip
RUN pip3 --no-cache-dir install pytest

# Create directories and set permissions
RUN mkdir -p /home/user/ml && \
    chmod 755 /home/user && \
    chmod 755 /home/user/ml

# Create the iris SQLite database
RUN cat <<'SQL' | sqlite3 /home/user/ml/iris.db
PRAGMA journal_mode=WAL;
CREATE TABLE iris (
    sepal_length REAL,
    sepal_width  REAL,
    petal_length REAL,
    petal_width  REAL,
    species      TEXT
);

INSERT INTO iris VALUES (5.0, 3.4, 1.5, 0.1, 'setosa');
INSERT INTO iris VALUES (5.1, 3.5, 1.4, 0.2, 'setosa');
INSERT INTO iris VALUES (4.9, 3.0, 1.4, 0.2, 'setosa');
INSERT INTO iris VALUES (6.0, 2.2, 5.0, 1.5, 'versicolor');
INSERT INTO iris VALUES (6.3, 2.9, 5.6, 1.8, 'virginica');
SQL

# Set database permissions
RUN chmod 644 /home/user/ml/iris.db

# Clean up apt caches
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH="/home/user/.local/bin:${PATH}"

# Container help / run message
CMD echo "Container for Iris minimum-petal-width exercise." && \
    echo "Use the sqlite3 CLI to query /home/user/ml/iris.db as described in the assignment."