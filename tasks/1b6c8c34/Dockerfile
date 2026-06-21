FROM ubuntu:22.04

# Help section from Apptainer %help
# This container sets up the environment for the SSH hardening task.

RUN set -e && \
    echo "Updating apt repositories and installing required packages..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 \
        ca-certificates && \
    echo "Installing pytest via pip..." && \
    pip3 install --no-cache-dir pytest && \
    echo "Creating initial directory structure and database..." && \
    mkdir -p /home/user

RUN sqlite3 /home/user/security_settings.db <<'SQL'
CREATE TABLE system_config (
        param TEXT PRIMARY KEY,
        val   TEXT NOT NULL
);
INSERT INTO system_config (param, val) VALUES ('permit_remote_root', 'yes');
SQL

RUN chmod 777 /home/user && \
    chmod 666 /home/user/security_settings.db && \
    rm -f /home/user/operation_done.log && \
    echo "Container build complete."

RUN chmod 755 /home/user

ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

CMD echo "This container sets up the environment for the SSH hardening task." && \
    echo "Open a shell inside the container to begin working:" && \
    exec /bin/bash