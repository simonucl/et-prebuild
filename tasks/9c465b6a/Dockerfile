FROM ubuntu:22.04

# This container provides the initial dataset and Python tooling (pytest) for
# the click-stream processing task.

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/data/raw && \
    chmod 777 /home/user/data

RUN cat <<'EOF' > /home/user/data/raw/user_events.tsv
user_id	event_type	timestamp
u01	click	2023-05-01T10:00:00Z
u02	view	2023-05-01T10:02:00Z
u01	click	2023-05-01T10:00:00Z
u03	purchase	2023-05-01T10:05:00Z
u02	view	2023-05-01T10:02:00Z
u04	click	2023-05-01T10:10:00Z
u02	click	2023-05-01T10:12:00Z
u03	view	2023-05-01T10:15:00Z
EOF

RUN chmod 644 /home/user/data/raw/user_events.tsv

RUN chmod 755 /home/user