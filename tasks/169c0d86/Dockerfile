FROM ubuntu:22.04

# HELP: Author: Data-Cleaning Exercise Base Image
# HELP: Description: Provides initial raw.csv and pytest for automated grading

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -d /home/user user

RUN mkdir -p /home/user/datasets && \
    chmod 0777 /home/user/datasets

RUN cat > /home/user/datasets/raw.csv <<'EOF'
id,name,age,score
1,Alice,30,85
2,Bob,,90
3,Charlie,25,
4,,27,88
5,David,22,92
EOF

RUN chmod 0644 /home/user/datasets/raw.csv

RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=utf-8

LABEL Author="Data-Cleaning Exercise Base Image"
LABEL Description="Provides initial raw.csv and pytest for automated grading"