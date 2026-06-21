FROM ubuntu:22.04

# Help text from %help
# This Apptainer image sets up the starting environment for the
# “credential-rotation” exercise. Only the original credential file exists;
# no rotation artefacts are present. Pytest is installed so the grader can
# run its checks.

ENV DEBIAN_FRONTEND=noninteractive

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/credentials && \
    chmod 0755 /home && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/credentials

RUN cat <<'EOF' > /home/user/credentials/app_secrets_2023-09-15.txt
legacy_client_id=deadbeef
legacy_client_secret=deadcafe
legacy_rotated_on=2023-09-15T12:00:00Z
EOF

RUN chmod 0644 /home/user/credentials/app_secrets_2023-09-15.txt && \
    chmod 755 /home/user

# Labels from %labels (chmod preserved above)
LABEL Author="Security Engineering Prep"
LABEL Description="Container providing the initial state for the credential-rotation task. Includes pytest for automated grading."