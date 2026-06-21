FROM ubuntu:22.04

# Install Python 3, pip and pytest (needed by the grading harness)
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial filesystem state for the exercise
# Create /home/user with open write permissions so the unprivileged
# learner process can add /home/user/analysis later on.
RUN mkdir -p /home/user/data && \
    chmod 0777 /home/user && \
    chmod 0755 /home/user/data

# Create the usage log with exact required content and permissions 644
RUN cat >/home/user/data/usage.log <<'EOF'
serverA 2023-07-01 24
serverB 2023-07-01 67
serverC 2023-07-01 53
serverA 2023-07-02 21
serverB 2023-07-02 79
serverC 2023-07-02 48
serverA 2023-07-03 35
serverB 2023-07-03 73
serverC 2023-07-03 64
EOF

RUN chmod 0644 /home/user/data/usage.log

# Put Python on PATH explicitly (usually already, but be safe)
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Labels
LABEL Author="Capacity-planner exercise container"
LABEL Description="Provides initial state and pytest for CPU peak task."

# Default entrypoint does nothing; container is only a workspace
CMD ["/bin/bash"]