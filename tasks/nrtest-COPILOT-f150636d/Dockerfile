FROM ubuntu:24.04

# trsi: pre-create harbor mount points world-writable so non-root-USER envs can be staged
USER root
RUN mkdir -p /solution /tests /logs && chmod 1777 /solution /tests /logs

# dpkg (the canonical Debian version-comparison tool) ships in the base image.
# python3 is needed by the agent's tooling and by the verifier.
RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 dpkg bash coreutils \
    && rm -rf /var/lib/apt/lists/*

# Stage the task's starting state: a read-only raw version feed under the pool.
RUN useradd -m -s /bin/bash user || true
RUN mkdir -p /home/user/pool
COPY versions.txt /home/user/pool/versions.txt
RUN chown -R user:user /home/user && chmod 0444 /home/user/pool/versions.txt

WORKDIR /home/user
USER user
