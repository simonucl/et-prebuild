FROM ubuntu:22.04

# Help / runscript notes from Apptainer
# Container for SQL optimisation exercise.
# Python and pytest will be available in PATH.

LABEL Author="Exercise Template Generator"
LABEL Description="Base image for SQL optimisation task with pytest pre-installed."

ENV HOME=/home/user

RUN set -e && \
    echo "Updating package lists and installing Python + pip ..." && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/projects/sql_work

RUN cat <<'EOF' >/home/user/projects/sql_work/original.sql
-- original.sql
CREATE TABLE employees (
    id INT PRIMARY KEY,
    name TEXT,
    department TEXT
);

SELECT * FROM employees WHERE department = 'Engineering';
EOF

RUN chmod 644 /home/user/projects/sql_work/original.sql && \
    chmod 755 /home/user /home/user/projects /home/user/projects/sql_work