FROM ubuntu:22.04

# Base tools
RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update -y && \
    apt-get install -y python3 python3-pip sqlite3 && \
    pip3 install --no-cache-dir pytest

# Create dedicated, non-privileged user "user" (UID/GID 1000)
RUN if ! id -u user >/dev/null 2>&1; then \
        groupadd -g 1000 user && \
        useradd -m -u 1000 -g 1000 -s /bin/bash user; \
    fi

# Directory structure with correct permissions
RUN install -o user -g user -m 770 -d /home/user/pipelines && \
    install -o user -g user -m 770 -d /home/user/pipelines/logs

# Create the SQL initialization file
RUN cat >/tmp/init_builds.sql <<'SQL'
CREATE TABLE builds (
    id INTEGER PRIMARY KEY,
    platform TEXT,
    status TEXT,
    timestamp TEXT
);

INSERT INTO builds VALUES
(40, 'ios',      'success', '2024-04-29T08:11:00Z');
INSERT INTO builds VALUES
(41, 'android',  'failed',  '2024-04-29T09:03:00Z');
INSERT INTO builds VALUES
(42, 'android',  'queued',  '2024-04-29T10:27:00Z');
INSERT INTO builds VALUES
(43, 'ios',      'queued',  '2024-04-29T10:41:00Z');
SQL

# Initialize the SQLite database and set permissions
RUN chown user:user /tmp/init_builds.sql && \
    su - user -c "sqlite3 /home/user/pipelines/app_builds.db < /tmp/init_builds.sql" && \
    rm /tmp/init_builds.sql && \
    chown user:user /home/user/pipelines/app_builds.db && \
    chmod 660 /home/user/pipelines/app_builds.db

# Set permissions on home directory
RUN chmod 755 /home/user

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

WORKDIR /home/user

CMD ["/bin/bash"]