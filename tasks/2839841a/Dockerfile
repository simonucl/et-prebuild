FROM ubuntu:22.04

# Help:
# This container sets up the initial state for the “Java artifacts
# frequency report” assignment. pytest is pre-installed so that the
# automated grader can validate the environment.

RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/project/artifacts && \
    chmod 700 /home/user/project && \
    chmod 700 /home/user/project/artifacts

RUN cat > /home/user/project/artifacts/list.txt <<'EOF'
artifact-alpha-1.0.0.jar
artifact-beta-2.1.0.jar
artifact-alpha-1.0.0.jar
artifact-gamma-3.3.7.jar
artifact-alpha-1.0.0.jar
artifact-beta-2.1.0.jar
artifact-delta-4.0.0.jar
artifact-epsilon-5.2.1.jar
artifact-gamma-3.3.7.jar
artifact-gamma-3.3.7.jar
artifact-beta-2.1.0.jar
artifact-delta-4.0.0.jar
artifact-beta-2.1.0.jar
EOF

RUN chmod 644 /home/user/project/artifacts/list.txt

RUN if [ -d /home/user/project/reports ]; then rm -rf /home/user/project/reports; fi

RUN chmod 755 /home/user