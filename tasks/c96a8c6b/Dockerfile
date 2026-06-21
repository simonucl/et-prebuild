FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip locales && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pytest

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen en_US.UTF-8

RUN mkdir -p /home/user/releases

RUN chmod 777 /home/user && \
    chmod 777 /home/user/releases

RUN cat >/home/user/releases/deployments.csv <<'EOF'
id,project,version,environment,status,release_date
1,frontend,1.4.2,staging,completed,2024-01-12
2,backend,2.3.0,production,pending,2024-03-05
3,api,3.1.1,staging,pending,2024-03-11
4,billing,4.0.0,production,aborted,2024-02-09
5,frontend,1.4.3,production,pending,2024-03-14
6,worker,0.9.8,staging,completed,2024-02-28
EOF

RUN chmod 644 /home/user/releases/deployments.csv

ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV LANGUAGE=en_US:en