FROM ubuntu:22.04

# Labels
LABEL Author="Container build script"
LABEL Purpose="Sets up initial state for the CSV + diagnostics exercise"

# -----------------------------------------------------------------
# Basic tooling and Python test framework
# -----------------------------------------------------------------
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        iputils-ping \
        inetutils-traceroute \
        net-tools && \
    pip3 install --no-cache-dir pytest

# -----------------------------------------------------------------
# Seed data for the exercise
# -----------------------------------------------------------------
# Create the directory tree that must already exist when the learner
# starts.  Do NOT create any of the artefacts the learner is supposed
# to produce.
RUN mkdir -p /home/user/site/config

# Initial CSV: header + two user records (alice, bob) — NO charlie yet.
RUN cat > /home/user/site/config/users.csv <<'EOF'
username,email,role
alice,alice@example.com,editor
bob,bob@example.com,viewer
EOF

# -----------------------------------------------------------------
# Permissions
# -----------------------------------------------------------------
# The learner will not have root inside the container, so make sure
# everything under /home/user is writable by any UID.
RUN chmod -R a+rwx /home/user && \
    chmod a+rw /home/user/site/config/users.csv

# Environment
ENV PATH=/usr/local/bin:/usr/bin:/bin