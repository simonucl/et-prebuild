FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        python3-wheel && \
    pip3 install --no-cache-dir pytest

# Set up directory tree
RUN mkdir -p /home/user && \
    chmod 0777 /home/user && \
    mkdir -p /home/user/project && \
    echo "Sample file 1" > /home/user/project/file1.txt && \
    echo "Top secret" > /home/user/project/secret.txt && \
    chmod 0644 /home/user/project/file1.txt && \
    chmod 0600 /home/user/project/secret.txt

# Clean apt caches
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Ensure correct permissions at runtime
RUN chmod 755 /home/user

ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Help (from %help)
# Container for the permissions auditing exercise.

CMD /bin/sh -c "echo 'Container for the permissions auditing exercise.' && echo 'Invoke your preferred shell or command to begin.'"