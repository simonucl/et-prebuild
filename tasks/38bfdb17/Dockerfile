FROM ubuntu:22.04

# Help documentation:
# This container provides the initial state for a cloud-migration
# exercise.  It includes:
#   • Ubuntu 22.04 base OS
#   • sqlite3 CLI
#   • pytest (for the autograder)
#   • Pre-populated /home/user/migration/source_app.db containing
#     a 3-row 'customers' table.
# All filesystem permissions are relaxed so that the non-privileged
# evaluation user can create, modify, and inspect files as required.

# Install required system packages
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        sqlite3 \
        ca-certificates \
        build-essential

# Install pytest for the validation test-suite
RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest

# Prepare initial filesystem state expected by the autograder
# Create /home/user and ensure it is writable by *any* user that the
# container might be executed under.
RUN mkdir -p /home/user && \
    chmod 777 /home/user

# Create the migration directory structure (only the root dir; backup
# sub-dir must NOT exist yet).
RUN mkdir -p /home/user/migration && \
    chmod 777 /home/user/migration

# Seed the on-prem "source" database.
RUN sqlite3 /home/user/migration/source_app.db <<EOF
BEGIN;
CREATE TABLE customers (
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);
INSERT INTO customers (id, name, email) VALUES
    (1, 'Alice Chen',  'alice.chen@example.com'),
    (2, 'Bob Gupta',   'bob.gupta@example.com'),
    (3, 'Carla Diaz',  'carla.diaz@example.com');
COMMIT;
EOF

# Make sure every user can read the DB and write into the directory
RUN chmod 666 /home/user/migration/source_app.db

# Final permission sweep so that any non-root UID running the tests
# can create new files/directories alongside our preparatory ones.
RUN chmod -R a+rwX /home/user

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Default command
CMD ["/bin/bash"]