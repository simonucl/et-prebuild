FROM ubuntu:22.04

LABEL Author="apptainer-task-generator"
LABEL Description="Initial state for \"daily uptime summary\" terminal-processing exercise."

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/monitoring && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/monitoring

RUN cat > /home/user/monitoring/uptime_report.csv <<'EOF'
timestamp,service_name,status,response_time_ms
2024-04-18T00:00:00Z,auth,UP,120
2024-04-18T00:00:00Z,payments,DOWN,0
2024-04-18T00:00:00Z,api,UP,95
2024-04-18T01:00:00Z,auth,UP,110
2024-04-18T01:00:00Z,payments,UP,210
2024-04-18T01:00:00Z,api,UP,100
2024-04-18T02:00:00Z,auth,DOWN,0
2024-04-18T02:00:00Z,payments,UP,190
2024-04-18T02:00:00Z,api,UP,98
EOF

RUN chmod 0644 /home/user/monitoring/uptime_report.csv && \
    rm -f /home/user/monitoring/daily_uptime_summary.txt || true

ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Help:
# This container supplies the starting environment for the "daily uptime
# summary" text-processing exercise.  It includes:
#
#   • /home/user/monitoring/uptime_report.csv  – the raw probe export
#   • pytest                                   – for automated grading
#
# Students should write shell commands inside the running container to produce
# /home/user/monitoring/daily_uptime_summary.txt exactly as described in the
# assignment.