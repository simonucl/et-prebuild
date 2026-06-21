FROM ubuntu:22.04

# Environment variables from %environment (none provided)

# Help text from %help
# This Docker image sets up the initial environment for the “Cluster Audit”
# programming task. It pre-installs Python 3, pytest, and creates the
# /home/user/cluster directory tree with the required users.txt files so that
# automated tests can verify the starting state.

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/cluster/nodes/node1 /home/user/cluster/nodes/node2 /home/user/cluster/nodes/node3

RUN cat <<EOF > /home/user/cluster/nodes/node1/users.txt
alice
bob
charlie
dave
EOF

RUN cat <<EOF > /home/user/cluster/nodes/node2/users.txt
alice
charlie
eve
frank
EOF

RUN cat <<EOF > /home/user/cluster/nodes/node3/users.txt
alice
bob
charlie
frank
EOF

RUN chmod 755 /home/user && \
    chmod -R 755 /home/user/cluster/nodes && \
    chmod 644 /home/user/cluster/nodes/node1/users.txt && \
    chmod 644 /home/user/cluster/nodes/node2/users.txt && \
    chmod 644 /home/user/cluster/nodes/node3/users.txt

LABEL Author="cluster-audit-setup"
LABEL Description="Provides the initial filesystem state for the Cluster Audit task."