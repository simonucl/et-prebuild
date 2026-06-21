FROM ubuntu:22.04

# Avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"
ENV LC_ALL="en_US.UTF-8"
ENV LANG="en_US.UTF-8"
ENV LANGUAGE="en_US:en"

# Update packages and install Python, pip, locales, certificates
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        ca-certificates \
        locales

# Generate UTF-8 locale
RUN locale-gen en_US.UTF-8

# Upgrade pip and install pytest
RUN python3 -m pip install --no-cache-dir --upgrade pip
RUN python3 -m pip install --no-cache-dir pytest

# Create reference data directory
RUN mkdir -p /home/user/reference

# Create the reference file using heredoc
RUN cat > /home/user/reference/perf_sample.dat <<'EOF'
CPU_MAX_OPS=7845
DISK_AVG_LAT_MS=3.45
MEM_AVAIL_MB=2034
EOF

# Set permissions
RUN chmod 755 /home/user && \
    chmod 755 /home/user/reference && \
    chmod 644 /home/user/reference/perf_sample.dat

# Labels
LABEL Author="Compliance Task Container"
LABEL Description="Base image for compliance benchmark task with reference data and pytest pre-installed."