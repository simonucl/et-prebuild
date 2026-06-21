FROM ubuntu:22.04

# Environment variables
ENV LC_ALL=C
ENV LANG=C
ENV PYTHONIOENCODING=utf8

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create initial directory structure
RUN mkdir -p /home/user/repos

# Create seed data for the task
RUN cat > /home/user/repos/scan_2023-07-01.log <<'EOF'
central|libalpha|2.1.0|x86_64|e1b71a5
central|libalpha|2.1.0|x86_64|e1b71a5
central|libalpha|2.3.1|arm64|a2c903f
central|libbeta|1.4.2|x86_64|ff3be91
central|toolset|5.0.0|x86_64|4abff29
local|libalpha|2.3.1|x86_64|b1c223d
local|libgamma|0.9.8|arm64|6d904aa
remote|libbeta|2.0.0|x86_64|7ea29fe
remote|toolset|5.1.1|arm64|c8d0aa7
remote|toolset|5.1.1|arm64|c8d0aa7
EOF

# Set permissions
RUN chmod 755 /home/user/repos && \
    chmod 644 /home/user/repos/scan_2023-07-01.log

# Ensure the output directory does NOT exist in the initial state
RUN rm -rf /home/user/output || true

WORKDIR /home/user

CMD ["/bin/bash"]