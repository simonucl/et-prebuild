FROM ubuntu:22.04

# Help:
# This container image sets up the initial state for the artifact-repository
# curation task. It provides the source upload log and Python/pytest for
# automated assessment.

LABEL Author="Prepared by ChatGPT – Apptainer task initialisation"

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

RUN set -eux && \
    mkdir -p /home/user && \
    chmod 755 /home/user

RUN cat <<'EOF' > /home/user/repository_uploads.log
2023-08-30 12:45:01 INFO repoA artifact aaa-1.0.jar uploaded successfully
2023-08-30 12:46:17 ERROR repoB artifact bbb-2.1.jar checksum mismatch
2023-08-31 09:15:33 WARN repoC artifact ccc-3.0.jar deprecated classifier
2023-09-01 08:00:14 INFO repoA artifact aaa-1.1.jar uploaded successfully
2023-09-01 08:02:55 ERROR repoA artifact aaa-1.1.jar checksum mismatch
2023-09-02 10:20:43 ERROR repoC artifact ccc-3.1.jar signature invalid
2023-09-02 11:00:00 INFO repoB artifact bbb-2.2.jar uploaded successfully
2023-09-03 07:30:22 INFO repoD artifact ddd-4.0.jar uploaded successfully
2023-09-03 07:32:10 ERROR repoD artifact ddd-4.0.jar checksum mismatch
2023-09-04 09:00:00 WARN repoA artifact aaa-1.2.jar large file size
2023-09-04 09:01:30 ERROR repoB artifact bbb-2.2.jar signature invalid
2023-09-05 13:22:17 INFO repoC artifact ccc-3.1.jar uploaded successfully
2023-09-05 13:23:02 ERROR repoC artifact ccc-3.1.jar timeout during replication
2023-09-05 13:25:47 INFO repoA artifact aaa-1.2.jar uploaded successfully
2023-09-06 15:40:00 ERROR repoE artifact eee-5.0.jar checksum mismatch
EOF

RUN chmod 644 /home/user/repository_uploads.log