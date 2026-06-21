FROM ubuntu:22.04

# Install Python and pytest (needed by the automated grader)
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Create the required directory hierarchy
RUN mkdir -p /home/user/docs/logs

# Create /home/user/docs/logs/app1.log
RUN cat > /home/user/docs/logs/app1.log <<'EOF'
INFO Starting application
WARNING Disk space almost full
ERROR Failed to open configuration
INFO Retrying startup
ERROR Aborted
EOF

# Create /home/user/docs/logs/app2.log
RUN cat > /home/user/docs/logs/app2.log <<'EOF'
INFO Initialising
INFO Running main loop
INFO Shutdown complete
EOF

# Create /home/user/docs/logs/app3.log
RUN cat > /home/user/docs/logs/app3.log <<'EOF'
ERROR Crash detected
WARNING Possible memory leak
ERROR Stack trace follows
WARNING Memory leak suspected
INFO Attempting restart
INFO Restart successful
EOF

# Ensure all users can read the logs and write future artefacts
RUN chmod -R a+rX /home/user && \
    chmod a+w /home/user /home/user/docs /home/user/docs/logs && \
    chmod 755 /home/user

# Labels
LABEL Author="Singularity Task Setup"
LABEL Description="Environment for release-notes statistics exercise"

# Help information (as comments):
# This container provides the initial workspace for the release-notes
# statistics task. Three example *.log files are placed under:
#     /home/user/docs/logs/
# Students must analyse these logs and create the specified CSV summary.