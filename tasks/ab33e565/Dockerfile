# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help / runscript equivalent
# Container for Release Engineering task. Use it with an interactive shell or run commands directly.

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir --upgrade pytest && \
    mkdir -p /home/user/releases

RUN cat <<'EOF' >/home/user/releases/release_log.csv
ID,Version,Commit,Date,Environment
1,2.3.0,5ad88f9,2023-04-17,staging
2,2.3.0,5ad88f9,2023-04-18,production
3,2.3.1,a71e3dd,2023-05-01,staging
4,2.3.1,a71e3dd,2023-05-02,production
5,2.2.5,cd891ee,2023-03-10,production
6,2.4.0,ab123df,2023-06-11,staging
7,2.4.0,ab123df,2023-06-12,production
8,2.5.0-beta,bad1337,2023-07-01,staging
EOF

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked chmod 755 /home/user/releases && \
    chmod 644 /home/user/releases/release_log.csv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH