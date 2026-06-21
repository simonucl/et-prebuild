FROM ubuntu:22.04

# Help text
# This container provides the starting environment for the credential-rotation task.
# Contents:
# - /home/user/secure_api/token.json (immutable credential source)
# - python3, pip, and pytest
# - curl for retrieving the JSON via file:// URI
# Working directory /home/user is writable.

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        curl \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user

RUN install -d -m 0755 /home/user/secure_api

RUN printf '{"new_token":"xyz789","expires_in":3600}' > /home/user/secure_api/token.json

RUN chmod 0644 /home/user/secure_api/token.json

RUN chmod 755 /home/user

ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

CMD echo "Container ready. Use this image to work on the credential rotation task."