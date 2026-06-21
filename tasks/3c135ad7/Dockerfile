FROM ubuntu:22.04

# Help section (from %help not provided but placeholder)
# Converted from Apptainer definition using localimage ubuntu_22.04.sif

ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pytest

RUN mkdir -p /home/user/infra-config/config

RUN cd /home/user/infra-config && \
    git init --initial-branch=main . && \
    git config user.name "Initial Committer" && \
    git config user.email "committer@example.com" && \
    git config --system --add safe.directory /home/user/infra-config

RUN cat <<'EOF' > /home/user/infra-config/config/serviceA.yml
service_name: serviceA
replicas: 3
image: serviceA:1.2.0
EOF

RUN cd /home/user/infra-config && \
    git add config/serviceA.yml && \
    git commit -m "Initial commit for serviceA configuration"

RUN chmod -R a+rwX /home/user

RUN chmod 755 /home/user

CMD ["bash"]