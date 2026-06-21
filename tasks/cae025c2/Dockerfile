FROM ubuntu:22.04

RUN set -eux && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    if ! id -u user >/dev/null 2>&1; then \
        useradd -m -s /bin/bash user; \
    fi && \
    mkdir -p /home/user && \
    chown -R user:user /home/user && \
    mkdir -p /usr/local/bin

RUN cat <<"EOF" >/usr/local/bin/docker
#!/usr/bin/env bash
# Lightweight stub emulating a subset of the Docker CLI
set -e

EXPECTED_ID="87e5c1b4a2d3"

case "$1" in
  ps)
    # Expected usage:
    # docker ps --filter name=^/mysql-prod$ --format {{.ID}}
    shift
    if [[ "$1" == "--filter" && "$2" == "name=^/mysql-prod$" && "$3" == "--format" && "$4" == "{{.ID}}" ]]; then
        echo "$EXPECTED_ID"
    else
        echo "Unsupported arguments for docker ps" >&2
        exit 1
    fi
    ;;
  inspect)
    # Expected usage:
    # docker inspect -f {{.State.Running}} 87e5c1b4a2d3
    shift
    if [[ "$1" == "-f" && "$2" == "{{.State.Running}}" && "$3" == "$EXPECTED_ID" ]]; then
        echo "true"
    else
        echo "false"
    fi
    ;;
  version|--version)
    echo "Docker version 20.10.8"
    ;;
  *)
    echo "Unsupported docker command: $1" >&2
    exit 1
    ;;
esac
EOF

RUN chmod 755 /usr/local/bin/docker

ENV PATH=/usr/local/bin:$PATH

RUN chmod 755 /home/user

LABEL Maintainer="Apptainer Task Prep"
LABEL Description="Container for MySQL Docker ID retrieval task with pytest installed."