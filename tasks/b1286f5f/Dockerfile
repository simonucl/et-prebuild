FROM ubuntu:22.04

# Labels
LABEL Author="spec.generated"
LABEL Description="Container for quick permissions audit task. Contains baseline filesystem for the grading tests."

# Post installation
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        build-essential && \
    pip3 install --no-cache-dir pytest && \
    groupadd -g 1000 user && \
    useradd -m -u 1000 -g user -s /bin/bash user && \
    mkdir -p /home/user/projects/test_project && \
    mkdir -p /home/user/www && \
    echo "Public world-writable file" > /home/user/public.txt && \
    : > /home/user/projects/test_project/tmp_data.log && \
    echo "Personal notes" > /home/user/notes.txt && \
    echo 'print("Hello World")' > /home/user/projects/test_project/main.py && \
    mkdir -p /home/user/projects/private_secret && \
    chmod 0666 /home/user/public.txt && \
    chmod 0666 /home/user/projects/test_project/tmp_data.log && \
    chmod 0777 /home/user/www && \
    chmod 0644 /home/user/notes.txt && \
    chmod 0644 /home/user/projects/test_project/main.py && \
    chmod 0700 /home/user/projects/private_secret && \
    chown -R user:user /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH=/home/user/.local/bin:$PATH

# Set home directory permissions at runtime and define default command
RUN chmod 755 /home/user

CMD ["echo", "Container built for the world-writable audit task."]