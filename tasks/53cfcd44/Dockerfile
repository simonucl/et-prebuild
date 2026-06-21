# Author: credential-rotation-setup
# Description: Environment for API credential rotation exercise
# This container provides the initial state for the “credential rotation” exercise.
# Inside the container you will find:
#   /home/user/credential_rotation/
#       new_token.txt
#       fake_endpoint.json
# pytest is pre-installed for automated grading.

FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        curl \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/credential_rotation

RUN printf 'SECURE-TOKEN-998877\n' > /home/user/credential_rotation/new_token.txt

RUN cat <<'EOF' > /home/user/credential_rotation/fake_endpoint.json
{
  "result": "success"
}
EOF

RUN chmod 755 /home/user && \
    chmod 755 /home/user/credential_rotation && \
    chmod 644 /home/user/credential_rotation/new_token.txt && \
    chmod 644 /home/user/credential_rotation/fake_endpoint.json