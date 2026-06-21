# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels
LABEL Author="monitoring-setup"
LABEL Description="Environment pre-configured for the memory monitoring prototype task."

# Environment
ENV MON_HOME=/home/user

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eux \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        bash \
        procps \
        ca-certificates \
    && pip3 install --no-cache-dir pytest \
    && mkdir -p /home/user/monitoring/config /home/user/monitoring/logs \
    && echo 'THRESHOLD=75' > /home/user/monitoring/config/threshold.conf

RUN cat <<'EOF' > /home/user/monitoring/check_memory.sh
#!/usr/bin/env bash
set -e

CONFIG_DIR="/home/user/monitoring/config"
LOGS_DIR="/home/user/monitoring/logs"
CONF_FILE="${CONFIG_DIR}/threshold.conf"
LOG_FILE="${LOGS_DIR}/memory_alert.log"

# Ensure config exists
if [[ ! -f "${CONF_FILE}" ]]; then
    echo "Missing configuration file: ${CONF_FILE}" >&2
    exit 1
fi

# shellcheck disable=SC1090
source "${CONF_FILE}"

if [[ -z "${THRESHOLD}" ]]; then
    echo "THRESHOLD not set in ${CONF_FILE}" >&2
    exit 1
fi

if [[ "$1" == "--test" ]]; then
    TOTAL=1000
    USED=900
    PERC=90
    echo "[TEST] [ALERT] Memory usage is ${PERC}% (Used: ${USED}MB / Total: ${TOTAL}MB)" >> "${LOG_FILE}"
    chmod 755 /home/user

    exit 0
fi

TOTAL=$(free -m | awk '/Mem:/ {print $2}')
USED=$(free -m | awk '/Mem:/ {print $3}')

# Basic sanity check
if [[ -z "${TOTAL}" || -z "${USED}" ]]; then
    echo "Unable to parse memory statistics." >&2
    exit 1
fi

# Integer arithmetic with simple rounding
PERC=$(( (USED * 100 + TOTAL / 2) / TOTAL ))

if (( PERC > THRESHOLD )); then
    TS=$(date "+%F %T")
    echo "[${TS}] ALERT: Memory usage is ${PERC}% (Used: ${USED}MB / Total: ${TOTAL}MB)" >> "${LOG_FILE}"
fi
EOF

RUN chmod 755 /home/user/monitoring/check_memory.sh \
    && /home/user/monitoring/check_memory.sh --test

CMD echo "Container for monitoring prototype. Files are pre-populated under /home/user/monitoring."