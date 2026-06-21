# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help text from %help
# This Apptainer image sets up the initial state for the dev_pipeline task.
# Directories:
#   /home/user/dev_pipeline/
#     incoming/   (contains data_alpha.csv and data_beta.csv)
#     archive/    (empty)
#     file_manifest.txt with three filenames; data_gamma.csv intentionally missing.
# Pytest is pre-installed for automated grading.

ENV PATH=/usr/local/bin:/usr/bin:/bin

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update -qq && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && \
    mkdir -p /home/user/dev_pipeline/incoming && \
    mkdir -p /home/user/dev_pipeline/archive && \
    chmod 700 /home/user && \
    chmod 700 /home/user/dev_pipeline && \
    chmod 700 /home/user/dev_pipeline/incoming && \
    chmod 700 /home/user/dev_pipeline/archive

RUN cat <<'EOF' > /home/user/dev_pipeline/incoming/data_alpha.csv
alpha_col1,alpha_col2
1,2
EOF

RUN cat <<'EOF' > /home/user/dev_pipeline/incoming/data_beta.csv
beta_col1,beta_col2
3,4
EOF

RUN chmod 600 /home/user/dev_pipeline/incoming/data_alpha.csv && \
    chmod 600 /home/user/dev_pipeline/incoming/data_beta.csv

RUN printf 'data_alpha.csv\ndata_beta.csv\ndata_gamma.csv\n' > /home/user/dev_pipeline/file_manifest.txt && \
    chmod 600 /home/user/dev_pipeline/file_manifest.txt

RUN rm -f /home/user/dev_pipeline/processed.log /home/user/dev_pipeline/error.log

RUN chmod 755 /home/user

# Labels from %labels
LABEL Author="ChatGPT"
LABEL Description="Container for the dev_pipeline mini data-processing task."