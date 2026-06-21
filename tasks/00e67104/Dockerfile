FROM ubuntu:22.04

# Labels
LABEL Author="example"
LABEL Description="Environment for Mobile Build Warning Frequency task; includes pytest and pre-populated log file."

# Environment variables
ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=UTF-8

# Install Python and pytest
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends python3 python3-pip; \
    pip3 install --no-cache-dir pytest; \
    apt-get clean; \
    rm -rf /var/lib/apt/lists/*

# Create directory structure
RUN mkdir -p /home/user/build/logs && \
    mkdir -p /home/user/build/reports

# Create the log file
RUN cat > /home/user/build/logs/mobile_build.log <<'EOF'
INFO: Build started
WARNING: Unused resource
INFO: Checking dependencies
WARNING: Deprecated API usage
INFO: Running Lint
WARNING: Unused resource
ERROR: Missing keystore
WARNING: Missing translation
INFO: Compiling sources
WARNING: Deprecated API usage
INFO: Packaging APK
WARNING: Unused resource
ERROR: Build failed
WARNING: Large APK size
INFO: Build environment: Android-30
WARNING: Missing translation
INFO: Retrying build steps
WARNING: Deprecated API usage
INFO: Re-running unit tests
INFO: Build completed with warnings
WARNING: Unused resource
INFO: Archiving artifacts
INFO: Pipeline finished
EOF

# Set permissions
RUN chmod 755 /home/user && \
    chmod 755 /home/user/build && \
    chmod 755 /home/user/build/logs && \
    chmod 755 /home/user/build/reports && \
    chmod 644 /home/user/build/logs/mobile_build.log