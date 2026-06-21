# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python tooling and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip python3-setuptools locales && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Ensure UTF-8 locale
RUN locale-gen en_US.UTF-8

# Prepare filesystem state
RUN mkdir -p /home/user/ci_data

RUN cat <<'CSV' > /home/user/ci_data/build_results.csv
build_id,artifact,status
1001,service-api,success
1002,service-auth,failure
1003,website,success
1004,worker,success
CSV

RUN cat <<'CSV' > /home/user/ci_data/deployment_targets.csv
build_id,target_env
1001,prod
1003,staging
1004,prod
CSV

RUN chmod -R a+rwX /home/user

ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8

RUN chmod 755 /home/user