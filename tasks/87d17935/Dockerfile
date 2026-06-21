FROM ubuntu:22.04

# Help/description
# Container for the 'Archive Experiments' task.
# Pytest is available. Workspace prepared under /home/user.

# Environment variables
ENV PATH="/home/user/bin:${PATH}"

# Base tooling and Python/pytest
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 python3-pip cron \
        findutils tar gzip && \
    pip3 install --no-cache-dir pytest

# Create non-root user "user" (UID/GID 1000) and its home directory
RUN groupadd -g 1000 user || true && \
    useradd -m -u 1000 -g 1000 -s /bin/bash user || true

# Prepare initial experiment workspace - Base directories
RUN install -o user -g user -d /home/user/experiments && \
    install -o user -g user -d /home/user/archive && \
    install -o user -g user -d /home/user/logs && \
    install -o user -g user -d /home/user/bin

# Experiment sub-structure
RUN install -o user -g user -d /home/user/experiments/exp_alpha && \
    install -o user -g user -d /home/user/experiments/exp_beta && \
    install -o user -g user -d /home/user/experiments/exp_gamma

# Files inside the experiments
RUN echo "dummy alpha model" | install -o user -g user -m 644 /dev/stdin /home/user/experiments/exp_alpha/model.bin && \
    echo "dummy beta checkpoint" | install -o user -g user -m 644 /dev/stdin /home/user/experiments/exp_beta/model.chk && \
    echo '{"metric": 0.99}' | install -o user -g user -m 644 /dev/stdin /home/user/experiments/exp_gamma/metrics.json

# Set mtimes to exactly 10 days ago for all created artefacts
RUN TEN_DAYS_AGO=$(date -d '10 days ago' '+%Y%m%d%H%M.%S') && \
    chmod 755 /home/user && \
    touch -t "$TEN_DAYS_AGO" /home/user/experiments/exp_alpha && \
    touch -t "$TEN_DAYS_AGO" /home/user/experiments/exp_alpha/model.bin && \
    touch -t "$TEN_DAYS_AGO" /home/user/experiments/exp_beta && \
    touch -t "$TEN_DAYS_AGO" /home/user/experiments/exp_beta/model.chk && \
    touch -t "$TEN_DAYS_AGO" /home/user/experiments/exp_gamma && \
    touch -t "$TEN_DAYS_AGO" /home/user/experiments/exp_gamma/metrics.json

CMD ["bash", "-c", "echo 'Container for the Archive Experiments task.' && echo 'Pytest is available. Workspace prepared under /home/user.'"]