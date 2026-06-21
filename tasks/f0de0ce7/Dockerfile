FROM ubuntu:22.04

# Install runtime dependencies (Python + pytest)
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create required directory tree
RUN mkdir -p /home/user/firmware/configs && \
    mkdir -p /home/user/firmware/firewall

# Populate initial files
RUN printf 'API_KEY="DEADBEEFDEADBEEFDEADBEEFDEADBEEF"\n' \
    > /home/user/firmware/configs/device.conf

RUN { \
        printf 'ALLOW 22\n'; \
        printf 'ALLOW 8080\n'; \
        printf 'ALLOW 1883\n'; \
    } > /home/user/firmware/firewall/rules.conf

# Ensure absence of security_audit.log
RUN rm -f /home/user/security_audit.log

# Make directory writable
RUN chmod -R a+rwx /home/user && \
    chmod 755 /home/user

ENV PATH="/usr/local/bin:${PATH}"

CMD ["bash"]