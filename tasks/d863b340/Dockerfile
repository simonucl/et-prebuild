FROM ubuntu:22.04

# Labels
LABEL Author="OpenAI ChatGPT"
LABEL Description="Container with pre-populated MLOps experiment data and pytest for grading."

# System packages
RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        locales && \
    rm -rf /var/lib/apt/lists/*

# Python tooling
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest

# Create user home directory
RUN mkdir -p /home/user

# Pre-populate experiment folders and files
RUN BASE=/home/user/mlops/experiments && \
    mkdir -p "${BASE}/exp_alpha" "${BASE}/exp_beta" "${BASE}/exp_gamma" && \
    # exp_alpha
    printf 'alpha\n' > "${BASE}/exp_alpha/model.pt" && \
    printf '{"accuracy":0.91}\n' > "${BASE}/exp_alpha/metrics.json" && \
    printf 'epochs:10\n' > "${BASE}/exp_alpha/config.yaml" && \
    # exp_beta
    printf 'beta\n' > "${BASE}/exp_beta/model.pt" && \
    printf '{"accuracy":0.88}\n' > "${BASE}/exp_beta/metrics.json" && \
    printf 'epochs:20\n' > "${BASE}/exp_beta/config.yaml" && \
    printf 'needs_tuning\n' > "${BASE}/exp_beta/notes.txt" && \
    # exp_gamma
    printf 'gamma\n' > "${BASE}/exp_gamma/model.pt" && \
    printf '{"accuracy":0.93}\n' > "${BASE}/exp_gamma/metrics.json" && \
    printf 'epochs:15\n' > "${BASE}/exp_gamma/config.yaml"

# Permissions
RUN chmod 777 /home/user/mlops && \
    chmod 755 /home/user

WORKDIR /home/user

CMD ["sh", "-c", "echo 'This container is intended to be used in an educational autograder.' && echo 'Invoke your solution script or open a shell to begin.'"]