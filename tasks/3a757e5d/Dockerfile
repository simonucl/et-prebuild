FROM ubuntu:22.04

# Update package index and install required packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        iproute2 \
        ca-certificates

# Install pytest for the grading harness
RUN pip3 install --no-cache-dir pytest

# Prepare writable home directory for the student
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# Provide a non-privileged friendly stub for `iptables`
# The real `iptables` binary normally requires CAP_NET_ADMIN. To keep the
# exercise solvable for an unprivileged user, we install a lightweight
# wrapper that satisfies:
#   * `iptables --version`
#   * `iptables -L -n -v`   (treated as `-L`)
#   * `iptables -S`
# and returns representative, read-only output that contains the keywords
# required by the grader ("Chain INPUT", "-A INPUT", …).
RUN cat << 'EOF' > /usr/local/bin/iptables
#!/usr/bin/env bash
# Minimal stub for iptables used in the training container
cmd="$1"

case "$cmd" in
    --version)
        echo "iptables v1.8.7 (nf_tables) stub"
        ;;
    -S)
        cat <<'OUT'
-P INPUT ACCEPT
-P FORWARD ACCEPT
-P OUTPUT ACCEPT
-A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
-A INPUT -p tcp --dport 22 -j ACCEPT
OUT
        ;;
    -L)
        # Accept and ignore additional flags such as -n -v
        cat <<'OUT'
Chain INPUT (policy ACCEPT)
target     prot opt source               destination
ACCEPT     all  --  0.0.0.0/0            0.0.0.0/0

Chain FORWARD (policy ACCEPT)
target     prot opt source               destination

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination
OUT
        ;;
    *)
        echo "Stub iptables: unsupported argument set: $*" >&2
        exit 1
        ;;
esac
EOF

RUN chmod +x /usr/local/bin/iptables

# Set environment variables
# Ensure /usr/local/bin is searched first (default on Ubuntu, but reinforce)
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Labels
LABEL Author="Task Setup"
LABEL Purpose="Initial container state for firewall snapshot exercise"

# Help information (as comments):
# This container provides the minimal environment for the student to complete
# the "firewall snapshot" task. Tools available:
#   • iptables  (stub allowing non-root listing of rules)
#   • ss        (from iproute2)
#   • pytest    (for the grading harness)

WORKDIR /home/user