FROM ubuntu:22.04

# Install required software
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        patch && \
    pip3 install --no-cache-dir pytest

# Ensure home directory exists
RUN mkdir -p /home/user

# Create prerequisite directories
RUN mkdir -p /home/user/webapp && \
    mkdir -p /home/user/patches

# Provide the original (un-patched) configuration file
RUN cat > /home/user/webapp/settings.conf <<'EOF'
# WebApp configuration
HOST=localhost
PORT=8080
DEBUG=false
TIMEOUT=30
EOF

# Provide the patch file that the agent must apply later
RUN cat > /home/user/patches/settings.patch <<'EOF'
--- a/settings.conf
+++ b/settings.conf
@@ -1,5 +1,6 @@
+# WebApp configuration
 HOST=localhost
-PORT=8080
-DEBUG=false
+PORT=9090
+DEBUG=true
 TIMEOUT=30
+MAX_CONNECTIONS=100
EOF

# Make everything in /home/user writable by the unprivileged user
RUN chmod -R a+rwX /home/user

# Labels
LABEL Author="sandbox"
LABEL Description="Environment for Apply a configuration patch and record the outcome task"

# Help information (as comment):
# This container image provides the clean starting state for the
# task where a QA engineer must apply a configuration patch and
# record the outcome.