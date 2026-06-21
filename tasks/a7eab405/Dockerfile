# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help text from %help / %runscript
# Apptainer container for the MLOps artifact hand-off task.

ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        locales \
        ca-certificates \
        tar \
        coreutils && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8

RUN mkdir -p /home/user/experiments/run_2024_03_18

RUN printf 'accuracy:0.9125\n' > /home/user/experiments/run_2024_03_18/accuracy.txt

RUN printf 'loss:0.0873\n' > /home/user/experiments/run_2024_03_18/loss.txt

RUN cat > /home/user/experiments/run_2024_03_18/params.json <<'EOF'
{
  "learning_rate": 0.001,
  "batch_size": 32,
  "epochs": 10
}
EOF

RUN dd if=/dev/urandom of=/home/user/experiments/run_2024_03_18/model.bin bs=1024 count=1 status=none

RUN chmod 755 /home/user /home/user/experiments /home/user/experiments/run_2024_03_18 && \
    chmod 644 /home/user/experiments/run_2024_03_18/*