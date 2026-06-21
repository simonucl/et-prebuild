FROM ubuntu:22.04

# Help text
# This container pre-provisions the filesystem layout required for the
# Android-build channel-symlink exercise. Pytest is installed so that the
# verification suite can run inside the container.

# Label
LABEL Author="task-prep-automation"
# The following line from %labels is a command, not a label; converting as a RUN:
RUN chmod 755 /home/user || true

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/builds/android && \
    mkdir -p /home/user/builds/channels

# Create VERSION files
RUN mkdir -p /home/user/builds/android/1.2.0 && \
    cat <<EOF > /home/user/builds/android/1.2.0/VERSION
channel=stable
version=1.2.0
EOF

RUN mkdir -p /home/user/builds/android/1.3.0-beta && \
    cat <<EOF > /home/user/builds/android/1.3.0-beta/VERSION
channel=beta
version=1.3.0-beta
EOF

RUN mkdir -p /home/user/builds/android/1.4.0 && \
    cat <<EOF > /home/user/builds/android/1.4.0/VERSION
channel=stable
version=1.4.0
EOF

RUN mkdir -p /home/user/builds/android/2.0.0-alpha && \
    cat <<EOF > /home/user/builds/android/2.0.0-alpha/VERSION
channel=canary
version=2.0.0-alpha
EOF

RUN mkdir -p /home/user/builds/android/2.0.0 && \
    cat <<EOF > /home/user/builds/android/2.0.0/VERSION
channel=stable
version=2.0.0
EOF

# Channel symlinks
RUN ln -s /home/user/builds/android/1.4.0 /home/user/builds/channels/stable && \
    ln -s /home/user/builds/android/1.3.0-beta /home/user/builds/channels/beta

# Permissions
RUN chmod -R 0777 /home/user/builds