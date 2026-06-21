FROM ubuntu:22.04

# From Apptainer %help
# This Apptainer image provides the starting filesystem layout and tools
# needed for the 'log to CSV' exercise. Pytest is installed for the test
# harness, and the raw log file is populated under /home/user/projects/logs/.

LABEL Author="automation-workflow-specialist"
LABEL Description="Environment for log-processing command-line exercise with pytest pre-installed."

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/projects/logs

RUN cat > /home/user/projects/logs/raw_events.log << 'EOF'
EVENT|2023-09-01T10:12:45Z|alice|LOGIN_SUCCESS
EVENT|2023-09-01T10:15:01Z|bob|LOGIN_FAILURE
EVENT|2023-09-01T10:17:22Z|alice|FILE_UPLOAD
EVENT|2023-09-01T10:20:55Z|carol|LOGIN_SUCCESS
EVENT|2023-09-01T10:25:30Z|bob|LOGIN_SUCCESS
EVENT|2023-09-01T10:30:05Z|alice|LOGIN_SUCCESS
EVENT|2023-09-01T10:35:47Z|dave|FILE_DELETE
EVENT|2023-09-01T10:40:18Z|carol|LOGIN_FAILURE
EVENT|2023-09-01T10:45:00Z|bob|LOGIN_SUCCESS
EVENT|2023-09-01T10:50:10Z|alice|LOGIN_FAILURE
EOF

RUN chmod 0777 /home/user/projects/logs && \
    chmod 0666 /home/user/projects/logs/raw_events.log && \
    rm -f /home/user/projects/logs/login_success_events.csv /home/user/projects/logs/login_success_counts.csv && \
    chmod 755 /home/user

ENV PATH="/usr/bin:$PATH"
ENV PYTHONIOENCODING="UTF-8"
ENV LC_ALL="C.UTF-8"