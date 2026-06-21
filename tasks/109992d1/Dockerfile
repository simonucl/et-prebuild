FROM ubuntu:22.04

# Help: Container for Prometheus-client version logging exercise.
# Execute your one-liner inside this container as instructed.

# Install system dependencies
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip and install required Python packages
RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir \
        pytest \
        prometheus-client==0.19.0

# Prepare required directory structure for the exercise
RUN mkdir -p /home/user/observability/reports && \
    chmod -R 0777 /home/user

# Standard locale settings
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /home/user

CMD ["echo", "Container for Prometheus-client version logging exercise. Execute your one-liner inside this container as instructed."]