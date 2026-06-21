FROM ubuntu:22.04

# Install Python, pip and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        coreutils \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial filesystem state expected by the grader
# Create user home and artifacts directory
RUN mkdir -p /home/user/artifacts && \
    chmod 0777 /home/user /home/user/artifacts

# 1. app-debug.apk – empty file
RUN : > /home/user/artifacts/app-debug.apk

# 2. app-release.apk – single byte "a" (0x61) with no trailing newline
RUN echo -n 'a' > /home/user/artifacts/app-release.apk

# 3. expected_checksums.sha256 – two lines, "sha256  filename" format
RUN cat > /home/user/artifacts/expected_checksums.sha256 <<'EOF'
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  app-debug.apk
ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb  app-release.apk
EOF

# Make the initial files writable by whoever runs inside the container
RUN chmod 0666 /home/user/artifacts/app-debug.apk \
               /home/user/artifacts/app-release.apk \
               /home/user/artifacts/expected_checksums.sha256

# Set permissions on home directory
RUN chmod 755 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /home/user