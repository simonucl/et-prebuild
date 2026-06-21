FROM ubuntu:22.04

# Help / metadata
LABEL Author="Apptainer Task Setup"
LABEL Description="Environment for the deploy targets transformation exercise with pytest installed."

ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN set -e \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/deploy \
    && chmod 0777 /home/user /home/user/deploy

RUN cat >/home/user/deploy/targets.txt <<'EOF'
web-01
web-02
api-01
db-01
EOF

RUN chmod 0666 /home/user/deploy/targets.txt

RUN chmod 755 /home/user

CMD echo "Container for deploy targets transformation exercise."