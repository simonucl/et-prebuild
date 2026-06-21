FROM ubuntu:22.04

# Environment setup
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN set -e && \
    # Update APT index and install required system packages
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        curl && \
    # Install pytest for the grading framework
    pip3 install --no-cache-dir pytest && \
    # Create the mock_endpoints directory with the exact permissions 0755
    mkdir -p /home/user/mock_endpoints && \
    chmod 755 /home/user/mock_endpoints && \
    # Create release_info.json with the exact single-line JSON payload,
    # no trailing newline, and permissions 0644
    echo -n '{"version":"1.5.2","status":"ready"}' \
        > /home/user/mock_endpoints/release_info.json && \
    chmod 644 /home/user/mock_endpoints/release_info.json && \
    # Clean up APT caches to keep the image lean
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Container for release-check exercise. Open a shell to begin.
CMD ["echo", "Container for release-check exercise. Open a shell to begin."]