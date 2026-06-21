FROM ubuntu:22.04

# Help / description from labels section
# Author="Apptainer Task Builder"
# Description="Container for diagnostic capture exercise – includes pre-existing runtime.log and pytest for automated grading."

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/app/logs

RUN cat > /home/user/app/logs/runtime.log <<'EOF'
System initialized successfully
Connection pool ready
Listening on port 8080
EOF

RUN chmod 0644 /home/user/app/logs/runtime.log

RUN chmod 0755 /home/user /home/user/app /home/user/app/logs || true

LABEL Author="Apptainer Task Builder"
LABEL Description="Container for diagnostic capture exercise – includes pre-existing runtime.log and pytest for automated grading."