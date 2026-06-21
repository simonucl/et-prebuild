# Converted from Apptainer %help and %runscript
# Original runscript message:
# Apptainer container for the experiment-tracking task.
# Start an interactive shell to begin:

FROM ubuntu:22.04

# Install Python, pip, pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare workspace
RUN mkdir -p /home/user

RUN cat <<'EOF' > /home/user/sample_artifact.txt
This is a sample artifact file for the experiment.
EOF

RUN chmod 755 /home && \
    chmod 755 /home/user && \
    chmod 644 /home/user/sample_artifact.txt

# Environment setup (symlink + PATH)
RUN if [ ! -e /usr/bin/python ] && [ -e /usr/bin/python3 ]; then \
        ln -sf /usr/bin/python3 /usr/local/bin/python; \
    fi

ENV PATH=/usr/local/bin:$PATH

CMD ["/bin/bash"]