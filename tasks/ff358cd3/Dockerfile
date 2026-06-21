FROM ubuntu:22.04

# Install Python, pip, pytest, and update system
RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial filesystem state
RUN set -e && \
    BASE=/home/user/mobile_ci && \
    mkdir -p \
        ${BASE}/builds/android \
        ${BASE}/builds/ios \
        ${BASE}/tools \
        ${BASE}/reports && \
    touch ${BASE}/builds/android/app-release_1.2.1.apk && \
    touch ${BASE}/builds/android/app-release_1.2.2.apk && \
    touch ${BASE}/builds/android/app-release_1.2.3.apk && \
    touch ${BASE}/builds/ios/app-release_1.2.1.ipa && \
    touch ${BASE}/builds/ios/app-release_1.2.2.ipa && \
    touch ${BASE}/builds/ios/app-release_1.2.3.ipa && \
    touch ${BASE}/builds/ios/app-release_1.2.5.ipa && \
    find /home/user/mobile_ci -type d -exec chmod 755 {} + && \
    find /home/user/mobile_ci -type f -exec chmod 644 {} +

# Permissions adjustment from %environment
RUN chmod 755 /home/user

# Environment variables from %environment
ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

# Help text from %runscript
# Container for the mobile CI reporting task.
# Nothing to run by default. Open a shell or execute your scripts.