FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Task Prep Bot"
LABEL Description="Environment for Maven artifact extraction exercise"

# Help information (as comments):
# This container provides the starting point for the Maven artifact
# extraction task.  The build log is pre-populated in
# /home/user/build_logs/full_build.log and pytest is installed for the
# automated grader.

# Install Python tooling required by the autograder
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare the initial filesystem state for the learner
RUN mkdir -p /home/user/build_logs

RUN cat >/home/user/build_logs/full_build.log <<'EOF'
2024-01-23 10:15:33,123 [INFO] Fetching dependencies...
2024-01-23 10:15:35,456 [INFO] Artifact: commons-lang3-3.12.0.jar SHA256=aae3fc61d7
2024-01-23 10:15:36,001 [INFO] Artifact: guava-32.0.1.jar SHA256=bbeef1023a
2024-01-23 10:15:37,333 [WARN] Some minor warning
2024-01-23 10:15:38,789 [INFO] Artifact: my-app-1.2.1-SNAPSHOT.jar SHA256=caa12cc998
2024-01-23 10:15:40,111 [ERROR] Build failed unexpectedly.
EOF

# Ensure the learner (non-root runtime user) can freely modify /home/user
RUN chmod -R 0777 /home/user

WORKDIR /home/user

CMD ["bash", "-c", "chmod 755 /home/user && exec /bin/bash"]