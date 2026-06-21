# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help:
# Nothing to declare; defer to container defaults.

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN set -eux && \
    INCOMING_DIR="/home/user/etl_workspace/incoming" && \
    mkdir -p "${INCOMING_DIR}/extras" && \
    printf "month,visits\nJan,1023\n" > "${INCOMING_DIR}/january.csv" && \
    printf "month,visits\nFeb,1107\n" > "${INCOMING_DIR}/february.csv" && \
    printf "Raw CSV dump received from upstream." > "${INCOMING_DIR}/readme.txt" && \
    printf "note_id,text\n1,'late arrival'\n" > "${INCOMING_DIR}/extras/notes.csv"

RUN chmod -R a+rwX /home/user/etl_workspace

RUN chmod 755 /home/user