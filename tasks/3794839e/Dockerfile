FROM ubuntu:22.04

# Author: agent
# Description: Initial state for MLOps artifacts aggregation task. Installs pytest and creates the required experiment directory tree and artifacts.txt files under /home/user.

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN groupadd -g 1000 user && \
    useradd -m -u 1000 -g 1000 -s /bin/bash user

RUN install -d -o user -g user /home/user/mlops/experiments/exp_alpha && \
    install -d -o user -g user /home/user/mlops/experiments/exp_beta && \
    install -d -o user -g user /home/user/mlops/experiments/exp_gamma

RUN printf "%s\n" \
        "model_alpha_v1.pt" \
        "metrics_alpha_v1.json" \
        "config_alpha.yml" \
        > /home/user/mlops/experiments/exp_alpha/artifacts.txt && \
    chown user:user /home/user/mlops/experiments/exp_alpha/artifacts.txt && \
    chmod 0644 /home/user/mlops/experiments/exp_alpha/artifacts.txt

RUN printf "%s\n" \
        "model_beta_v2.pt" \
        "metrics_beta_v2.json" \
        "config_beta.yml" \
        "shared_vocab.txt" \
        > /home/user/mlops/experiments/exp_beta/artifacts.txt && \
    chown user:user /home/user/mlops/experiments/exp_beta/artifacts.txt && \
    chmod 0644 /home/user/mlops/experiments/exp_beta/artifacts.txt

RUN printf "%s\n" \
        "model_gamma_v3.pt" \
        "metrics_gamma_v3.json" \
        "config_gamma.yml" \
        "shared_vocab.txt" \
        > /home/user/mlops/experiments/exp_gamma/artifacts.txt && \
    chown user:user /home/user/mlops/experiments/exp_gamma/artifacts.txt && \
    chmod 0644 /home/user/mlops/experiments/exp_gamma/artifacts.txt

RUN chown -R user:user /home/user && chmod 755 /home/user

ENV PATH=/usr/local/bin:$PATH
ENV PYTHONUSERBASE=/home/user/.local
ENV PATH=/home/user/.local/bin:$PATH

CMD ["/bin/bash"]