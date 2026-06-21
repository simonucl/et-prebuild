FROM ubuntu:22.04

# Help text from %help
# This container provides the starting environment for the data-cleaning task.
# Raw datasets are located under /home/user/datasets/raw/.
# Pytest is installed system-wide for automated grading.

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/datasets/raw

RUN cat <<'EOF' > /home/user/datasets/raw/experiment_A.csv
ID,Value
A1,10
A2,15
A3,N/A
A4,20
EOF

RUN cat <<'EOF' > /home/user/datasets/raw/experiment_B.csv
ID,Value
B1,5
B2,8
B3,11
B4,N/A
B5,12
EOF

RUN chmod -R a+rwx /home/user

LABEL Author="Apptainer Task Prep"
LABEL Description="Container pre-configured with raw CSV files and pytest for the data-cleaning exercise."