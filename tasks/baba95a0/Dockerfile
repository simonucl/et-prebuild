# syntax=docker/dockerfile:1
# Container for the “dev_project” re-organisation exercise.
# The project starts with four loose files in /home/user/dev_project and
# no sub-directories. Pytest is installed for automated evaluation.

FROM ubuntu:22.04

ENV HOME=/home/user

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/dev_project && \
    cd /home/user/dev_project && \
    printf '# Placeholder application code\n' > app.py && \
    printf '# Placeholder test file\n'        > test_app.py && \
    printf 'Project README\n'                > README.txt && \
    printf 'Changelog\n'                     > changelog.md && \
    chmod -R a+rwx /home/user/dev_project

RUN chmod 755 /home/user

CMD ["/bin/bash"]