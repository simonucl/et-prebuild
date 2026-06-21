FROM ubuntu:22.04

# Help section omitted (none provided)

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        make \
        tar \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/artifacts && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/artifacts && \
    printf 'Meeting notes for Q1.\n'   > /home/user/artifacts/notes.txt && \
    printf 'v1.0 – initial release.\n' > /home/user/artifacts/changelog.txt && \
    printf 'MIT License\n'             > /home/user/artifacts/license.txt && \
    chmod 0666 /home/user/artifacts/*.txt

ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Default runscript behavior: exec commands passed to container
CMD ["bash"]