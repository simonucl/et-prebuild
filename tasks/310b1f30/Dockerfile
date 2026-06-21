FROM ubuntu:22.04

# System packages and Python tooling
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        tzdata \
        locales && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create non-root working user
RUN groupadd -g 1000 user && \
    useradd -m -u 1000 -g 1000 -s /bin/bash user

# Set up initial filesystem required for the exercise
RUN PIPELINE_DIR="/home/user/mobile-pipeline" && \
    mkdir -p "${PIPELINE_DIR}/logs"

# Create build_android.sh with deliberately insecure mode 777
RUN cat > /home/user/mobile-pipeline/build_android.sh <<'EOF'
#!/bin/bash
# Dummy build script placeholder
echo "Building Android…"
EOF

RUN chmod 777 /home/user/mobile-pipeline/build_android.sh

# Set logs directory with mode 755
RUN chmod 755 /home/user/mobile-pipeline/logs

# Create release_signing.key with mode 644 and dummy content
RUN echo "FAKE-ANDROID-RELEASE-KEY" > /home/user/mobile-pipeline/release_signing.key && \
    chmod 644 /home/user/mobile-pipeline/release_signing.key

# Ensure ownership by the non-root user so the student can modify them
RUN chown -R 1000:1000 /home/user && \
    chmod 755 /home/user

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Default command
CMD echo "Container for Android permission challenge." && echo "Switch to the 'user' account to begin."