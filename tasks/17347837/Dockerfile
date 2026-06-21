FROM ubuntu:22.04

# Help / runscript text
# Container for the artifact-manager task. Use an interactive shell to begin.

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

# Install Python and pytest
RUN set -e \
    && apt-get update -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
    && pip3 install --no-cache-dir pytest \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Prepare filesystem state
RUN set -e \
    && mkdir -p /home/user/artifacts-source \
    && printf 'ALPHA\n' > /home/user/artifacts-source/alpha.bin \
    && printf 'BETA\n'  > /home/user/artifacts-source/beta.bin \
    && chmod 755 /home/user \
    && chmod 755 /home/user/artifacts-source \
    && chmod 644 /home/user/artifacts-source/alpha.bin /home/user/artifacts-source/beta.bin

CMD echo "Container for the artifact-manager task. Use an interactive shell to begin."