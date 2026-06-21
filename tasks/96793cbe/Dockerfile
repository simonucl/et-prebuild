FROM ubuntu:22.04

# Help / metadata
# Author "Auto-generated for DNS audit task"

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

RUN if ! id -u user >/dev/null 2>&1; then \
        useradd -m -u 1000 -s /bin/bash user; \
    fi

RUN chmod 0755 /home/user

RUN install -d -m 0755 /home/user/dns_testset

RUN printf 'localhost=127.0.0.1\nip6-localhost=::1' \
        > /home/user/dns_testset/expected_hosts.txt && \
    chmod 0644 /home/user/dns_testset/expected_hosts.txt

RUN chown -R 1000:1000 /home/user/dns_testset

RUN rm -rf /home/user/audit || true

RUN chmod 755 /home/user

ENV PATH="/home/user/.local/bin:${PATH}"

LABEL Author="Auto-generated for DNS audit task"