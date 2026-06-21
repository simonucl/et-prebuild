FROM ubuntu:22.04

# Author MLOps-Task-Setup

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/mlops/artifacts/experiments

RUN cat <<'EOF' > /home/user/mlops/artifacts/experiments/alpha_metrics.tsv
epoch	run_id	alpha_acc	alpha_loss
1	ALPHA-001	0.80	0.45
2	ALPHA-002	0.82	0.40
3	ALPHA-003	0.83	0.38
EOF

RUN cat <<'EOF' > /home/user/mlops/artifacts/experiments/beta_metrics.tsv
epoch	run_id	beta_acc	beta_loss
1	BETA-001	0.78	0.50
2	BETA-002	0.79	0.48
3	BETA-003	0.81	0.44
EOF

RUN chmod 644 /home/user/mlops/artifacts/experiments/*.tsv && \
    chmod -R 755 /home/user

RUN if ! id -u user >/dev/null 2>&1; then useradd -m -u 1000 -s /bin/bash user; fi

RUN chmod 755 /home/user