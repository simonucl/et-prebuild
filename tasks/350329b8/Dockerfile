FROM ubuntu:22.04

# Help / runscript (informational only)
# Container for DevSecOps policy-as-code exercise.
# Enter the container and follow the instructions to generate the audit log.

ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        locales && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/policies && \
    chmod 0777 /home/user

RUN cat <<'EOF' >/home/user/policies/policy-001.yaml
id: policy-001
name: ensure-ssh-protocol-2
enabled: true
EOF

RUN cat <<'EOF' >/home/user/policies/policy-002.yaml
id: policy-002
name: disallow-root-login
enabled: false
EOF

RUN cat <<'EOF' >/home/user/policies/policy-003.yaml
id: policy-003
name: enforce-password-complexity
# NOTE: intentionally missing "enabled" key
EOF

RUN chmod 0644 /home/user/policies/policy-*.yaml

RUN chmod 755 /home/user