FROM ubuntu:22.04

# Install Python 3, pip, and pytest
RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create data directory
RUN mkdir -p /home/user/api_test/data

# Create the benchmark file
RUN cat > /home/user/api_test/data/response_samples.txt <<'EOF'
request_id,time_ms
1,120
2,110
3,130
4,115
5,140
6,125
EOF

# Ensure permissions
RUN chmod -R a+rwX /home/user

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"
ENV PYTHONDONTWRITEBYTECODE=1

# Labels
LABEL Author="Apptainer Task Preparer"
LABEL Description="Container for API performance summary exercise with pytest pre-installed."