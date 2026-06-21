# syntax=docker/dockerfile:1
# Based on Apptainer: Bootstrap: localimage / From: ./ubuntu_22.04.sif
# Using closest Docker equivalent
FROM ubuntu:22.04

# --- %post ---
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && \
    chmod 0777 /home/user

RUN mkdir -p /home/user/site && \
    chmod 0777 /home/user/site

RUN cat <<'EOF' > /home/user/site/accounts.tsv
101	alice	alice@example.com	admin
102	bob	bob@domain.com	editor
103	carol	carol@mail.net	viewer
104	dave	dave@site.org	editor
EOF

RUN chmod 0644 /home/user/site/accounts.tsv

# --- %environment ---
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

RUN chmod 755 /home/user

# --- %labels ---
LABEL Author="Automatic container setup for coding task"
LABEL Description="Provides initial state and pytest for the user_email.csv extraction exercise."