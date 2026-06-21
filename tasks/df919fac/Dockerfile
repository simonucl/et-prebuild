FROM ubuntu:22.04

# Labels
LABEL Author="Auto-generated performance alert container"

# Help section as comments
# This container comes pre-loaded with the required monitoring module
# (perf_alert.sh), configuration file (thresholds.conf) and alerts log
# (alerts.log) under /home/user/monitoring as per the assignment
# specification. Pytest is installed for automated verification.

# Environment
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Basic tools & pytest
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        bash && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Create required directory structure
RUN mkdir -p /home/user/monitoring && \
    chmod 777 /home /home/user /home/user/monitoring

# Create thresholds.conf
RUN cat > /home/user/monitoring/thresholds.conf <<'EOF'
CPU_THRESHOLD=80
MEM_THRESHOLD=70
EOF

RUN chmod 666 /home/user/monitoring/thresholds.conf

# Create perf_alert.sh
RUN cat > /home/user/monitoring/perf_alert.sh <<'EOF'
#!/bin/bash
# ------------------------------------------------------------------
# Minimal self-contained performance alert script
# ------------------------------------------------------------------
MON_DIR="/home/user/monitoring"
CONF="${MON_DIR}/thresholds.conf"
ALERT_LOG="${MON_DIR}/alerts.log"

# Load thresholds from configuration
if [[ -f "$CONF" ]]; then
    # shellcheck source=/dev/null
    source "$CONF"
else
    echo "Configuration file not found: $CONF" >&2
    exit 1
fi

# Ensure the alert log exists
touch "$ALERT_LOG"

# --------------------------------------------------------------
# CPU Monitor
# --------------------------------------------------------------
cpu_monitor() {
    # Read initial CPU stats
    read _ user nice system idle iowait irq softirq steal guest < /proc/stat
    prev_idle=$idle
    prev_total=$((user+nice+system+idle+iowait+irq+softirq+steal))

    while true; do
        sleep 1
        read _ user nice system idle iowait irq softirq steal guest < /proc/stat
        idle_diff=$((idle - prev_idle))
        total=$((user+nice+system+idle+iowait+irq+softirq+steal))
        total_diff=$((total - prev_total))

        if [ "$total_diff" -gt 0 ]; then
            usage=$(( 100 * (total_diff - idle_diff) / total_diff ))
        else
            usage=0
        fi

        if [ "$usage" -ge "$CPU_THRESHOLD" ]; then
            ts=$(date "+[%Y-%m-%d %H:%M:%S]")
            echo "${ts} ALERT: {\"metric\":\"cpu\",\"value\":${usage},\"threshold\":${CPU_THRESHOLD}}" >> "$ALERT_LOG"
        fi

        prev_idle=$idle
        prev_total=$total
    done
}

# --------------------------------------------------------------
# Memory Monitor
# --------------------------------------------------------------
mem_monitor() {
    while true; do
        sleep 1
        mem_total=$(grep -m1 -i "^MemTotal:" /proc/meminfo | awk '{print $2}')
        mem_avail=$(grep -m1 -i "^MemAvailable:" /proc/meminfo | awk '{print $2}')

        [ -z "$mem_total" ] && continue
        [ -z "$mem_avail" ] && continue

        used_kb=$((mem_total - mem_avail))
        usage=$(( 100 * used_kb / mem_total ))

        if [ "$usage" -ge "$MEM_THRESHOLD" ]; then
            ts=$(date "+[%Y-%m-%d %H:%M:%S]")
            echo "${ts} ALERT: {\"metric\":\"memory\",\"value\":${usage},\"threshold\":${MEM_THRESHOLD}}" >> "$ALERT_LOG"
        fi
    done
}

# ------------------------------------------------------------------
# Spawn samplers in parallel
# ------------------------------------------------------------------
cpu_monitor &
CPU_PID=$!
mem_monitor &
MEM_PID=$!

# Graceful shutdown on Ctrl-C
trap "kill $CPU_PID $MEM_PID 2>/dev/null; wait; exit 0" SIGINT

# Wait for children
wait
EOF

RUN chmod 755 /home/user/monitoring/perf_alert.sh

# Create alerts.log with deterministic sample line
RUN echo '[2023-01-01 00:00:00] ALERT: {"metric":"cpu","value":99,"threshold":80}' > /home/user/monitoring/alerts.log && \
    chmod 666 /home/user/monitoring/alerts.log