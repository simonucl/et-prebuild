# Converted from Apptainer definition
FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/app

# requirements_old.txt
RUN cat >/home/user/app/requirements_old.txt <<'EOF'
requests==2.25.0
numpy==1.18.0
pandas==1.1.0
EOF

# requirements_new.txt
RUN cat >/home/user/app/requirements_new.txt <<'EOF'
requests==2.31.0
numpy==1.24.0
pandas==2.0.3
EOF

RUN chmod 644 /home/user/app/requirements_old.txt /home/user/app/requirements_new.txt

# Ensure update_logs directory does not exist
RUN rm -rf /home/user/update_logs

# General permissions
RUN chmod 755 /home/user && chmod 755 /home/user/app

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"
ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=UTF-8

# Labels
LABEL Author="agent-prep"
LABEL Description="Environment for dependency-comparison task, includes pytest and initial requirement files."