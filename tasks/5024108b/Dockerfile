# Author example
# Description Artifact-repository task base image with log fixture and pytest pre-installed.
# This Apptainer image provides the initial filesystem state for the
# “artifact-repository engineer” exercise. It contains the raw HTTP access
# log at /home/user/logs/artifact_audit.log and has pytest installed so that
# the automated grader can run its test suite. No report outputs are
# pre-created; students are expected to generate them.

FROM ubuntu:22.04

LABEL Author="example"
LABEL Description="Artifact-repository task base image with log fixture and pytest pre-installed."

RUN set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        python3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/logs

RUN cat <<'EOF' > /home/user/logs/artifact_audit.log
2024-07-20T10:15:42Z repo-core/org/example/libfoo-1.2.3.jar 200 -
2024-07-20T10:15:43Z repo-core/org/example/libbar-2.0.0.jar 404 Not Found
2024-07-20T10:16:01Z repo-proprietary/com/acme/widget-5.1.0.bin 500 Internal Server Error
2024-07-20T10:16:05Z repo-proprietary/com/acme/widget-5.1.0.sig 200 -
2024-07-20T10:17:22Z repo-dev/io/experiment/test-0.0.1-alpha.jar 404 Not Found
2024-07-20T10:18:55Z repo-core/org/example/libbaz-3.1.4.jar 200 -
2024-07-20T10:19:04Z repo-core/org/example/libbar-2.0.0-sources.jar 404 Not Found
EOF

RUN chmod 0644 /home/user/logs/artifact_audit.log && \
    chmod 0755 /home/user/logs && \
    chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8