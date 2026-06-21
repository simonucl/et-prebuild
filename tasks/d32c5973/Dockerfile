FROM ubuntu:22.04

# Author Release-Manager Exercise Container
# Container image for the "release-manager" assignment.
# Provides:
#   * Python 3 + pytest for grading
#   * Pre-created /home/user/releases/releases.csv as described in the spec
# The student's solution will run inside this image without root privileges.

# Update APT and install Python + pip
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install pytest for the grading test-suite
RUN pip3 install --no-cache-dir pytest

# Prepare initial filesystem state expected by the assignment
# Create the required CSV under /home/user/releases/
RUN mkdir -p /home/user/releases

RUN cat >/home/user/releases/releases.csv <<'EOF'
service,environment,version,status
auth,staging,1.4.3,ready
payments,production,2.1.0,hold
orders,staging,3.0.1,ready
notifications,production,1.9.5,ready
analytics,staging,2.2.8,hold
EOF

# Permissions:
# - /home/user must be writable by the (non-root) student so they can
#   create /home/user/deployment during the exercise.
# CSV needs only read access
RUN chmod 777 /home/user && \
    chmod 755 /home/user/releases && \
    chmod 644 /home/user/releases/releases.csv