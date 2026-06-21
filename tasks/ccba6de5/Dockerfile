FROM ubuntu:22.04

# Install Python and PyPI, then pytest for validation
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Prepare filesystem layout for the credential-rotation exercise
# ------------------------------------------------------------------
# Create the target home and secrets directory
RUN mkdir -p /home/user/.secrets

# Make sure the regular (non-root) runtime user can write there
RUN chmod 0777 /home/user && \
    chmod 0777 /home/user/.secrets

# Seed the "old" token file with the exact required contents
RUN printf "OLD_TOKEN_qwerty\n" > /home/user/.secrets/old_api_token.txt && \
    chmod 0666 /home/user/.secrets/old_api_token.txt

# Guarantee that no other artefacts from a previous build remain
RUN rm -f /home/user/.secrets/old_api_token.bak \
          /home/user/credential_rotation_benchmark.log || true

# Environment settings
ENV PATH="$PATH:/usr/local/bin"

# Note: chmod 755 /home/user from %environment is moved to a RUN command
# since ENV cannot execute commands
RUN chmod 755 /home/user