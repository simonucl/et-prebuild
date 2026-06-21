# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ---------------------------------------------------------------------
# Install required packages and pytest
# ---------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        sqlite3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ---------------------------------------------------------------------
# Create runtime user and its home directory
# ---------------------------------------------------------------------
RUN set -e && \
    USERNAME="user" && \
    USERHOME="/home/${USERNAME}" && \
    if ! id -u "${USERNAME}" >/dev/null 2>&1; then \
        groupadd --gid 1000 "${USERNAME}" && \
        useradd  --uid 1000 \
                 --gid 1000 \
                 --create-home \
                 --home-dir "${USERHOME}" \
                 --shell /bin/bash \
                 "${USERNAME}"; \
    fi && \
    mkdir -p "${USERHOME}" && \
    chown "${USERNAME}:${USERNAME}" "${USERHOME}"

# ---------------------------------------------------------------------
# Create and populate the SQLite helpdesk.db database
# ---------------------------------------------------------------------
RUN set -e && \
    USERNAME="user" && \
    USERHOME="/home/${USERNAME}" && \
    DB_PATH="${USERHOME}/helpdesk.db" && \
    cat <<'SQL_CMDS' | sqlite3 "${DB_PATH}"
PRAGMA foreign_keys = OFF;
BEGIN TRANSACTION;
CREATE TABLE tickets (
    id          INTEGER PRIMARY KEY,
    status      TEXT,
    assigned_to TEXT
);
INSERT INTO tickets (id, status, assigned_to) VALUES
    (1, 'open',   'unassigned'),
    (2, 'closed', 'alice'),
    (3, 'open',   'unassigned'),
    (4, 'open',   'bob'),
    (5, 'closed', 'unassigned'),
    (6, 'open',   'charlie');
COMMIT;
SQL_CMDS

RUN set -e && \
    USERNAME="user" && \
    USERHOME="/home/${USERNAME}" && \
    DB_PATH="${USERHOME}/helpdesk.db" && \
    chmod 0644 "${DB_PATH}" && \
    chown "${USERNAME}:${USERNAME}" "${DB_PATH}"

# ---------------------------------------------------------------------
# Environment setup
# ---------------------------------------------------------------------
RUN chmod 755 /home/user
ENV PATH="${PATH}:/home/user/.local/bin"

# ---------------------------------------------------------------------
# Labels (from %labels)
# ---------------------------------------------------------------------
LABEL Author="Apptainer build script" \
      Description="Environment for helpdesk ticket counting task with pre-populated SQLite database."

# ---------------------------------------------------------------------
# Default run command (from %runscript)
# ---------------------------------------------------------------------
CMD ["/bin/bash"]