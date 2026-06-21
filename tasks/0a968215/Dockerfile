FROM ubuntu:22.04

# Help section from %runscript
# Container for the security-hardening exercise.
# Invoke your shell or commands as needed.

ENV PATH="/home/user/.local/bin:${PATH}"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0777 /home/user || true

RUN if [ ! -f /home/user/.bashrc ]; then \
        touch /home/user/.bashrc && \
        echo "" >> /home/user/.bashrc ; \
    fi

RUN chmod 755 /home/user

CMD echo "Container for the security-hardening exercise." && \
    echo "Invoke your shell or commands as needed."