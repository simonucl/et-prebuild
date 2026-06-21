FROM ubuntu:22.04

# Labels
LABEL Author="example"
LABEL Description="Container providing the initial state for the API log archiving task."
LABEL Version="1.0"

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial filesystem state required by the tests
RUN mkdir -p /home/user/api_test/logs

# Create requests.log (exactly 38 bytes)
RUN printf 'GET /users\nPOST /users\nGET /users/123\n' \
    > /home/user/api_test/logs/requests.log

# Create responses.log (exactly 26 bytes)
RUN printf '200 OK\n201 Created\n200 OK\n' \
    > /home/user/api_test/logs/responses.log

# Ensure everything is world-readable (no root-only permissions)
RUN chmod -R a+rX /home/user

# Set working directory
WORKDIR /home/user

# Default command
CMD ["bash", "-c", "chmod 755 /home/user && echo 'Container for API log archiving task. Start an interactive shell.' && /bin/bash"]