FROM ubuntu:22.04

# %help and labels
LABEL Author="example@example.com"
LABEL Description="Container for checksum creation exercise – includes pytest and pre-seeded log file."

# Environment variables
ENV PYTHONIOENCODING=UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Install Python, pip, pytest, and set up filesystem
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/diagnostics && \
    printf 'abc' > /home/user/diagnostics/collect-logs.log && \
    chmod 755 /home/user && \
    chmod 755 /home/user/diagnostics && \
    chmod 644 /home/user/diagnostics/collect-logs.log

# Default command
CMD ["bash"]