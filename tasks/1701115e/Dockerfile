FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Task Prep"
LABEL Description="Environment for performance-log processing exercise"

# Help information (as comments):
# This container image provides the starting state for the "performance
# log processing" shell-scripting exercise.  The raw input file
# /home/user/logs/perf_data.log is present; none of the output artefacts
# exist yet.  Pytest is pre-installed for automated grading.

# Update APT metadata and install prerequisites
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip

# Install pytest for the grader
RUN pip3 install --no-cache-dir pytest

# Create the logs directory (reports directory must *not* exist yet)
RUN mkdir -p /home/user/logs && \
    chmod 755 /home/user && \
    chmod 755 /home/user/logs

# Populate the raw performance log with the exact 10 reference lines
RUN cat > /home/user/logs/perf_data.log <<'EOF'
2023-07-01T12:00:01Z appX latency_ms=123 cpu_pct=45.6 mem_mb=256
2023-07-01T12:00:02Z appY latency_ms=200 cpu_pct=78.9 mem_mb=512
2023-07-01T12:00:03Z appX latency_ms=150 cpu_pct=50.1 mem_mb=260
2023-07-01T12:00:04Z appY latency_ms=180 cpu_pct=70.3 mem_mb=500
2023-07-01T12:00:05Z appZ latency_ms=95  cpu_pct=30.0 mem_mb=128
2023-07-01T12:00:06Z appX latency_ms=110 cpu_pct=40.0 mem_mb=255
2023-07-01T12:00:07Z appZ latency_ms=105 cpu_pct=32.5 mem_mb=130
2023-07-01T12:00:08Z appY latency_ms=250 cpu_pct=85.0 mem_mb=520
2023-07-01T12:00:09Z appZ latency_ms=90  cpu_pct=29.5 mem_mb=127
2023-07-01T12:00:10Z appX latency_ms=200 cpu_pct=60.0 mem_mb=300
EOF

RUN chmod 644 /home/user/logs/perf_data.log