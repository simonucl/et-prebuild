FROM ubuntu:22.04

# From %post
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/app/current && \
    chmod 0777 /home/user && \
    echo "# placeholder" > /home/user/app/current/app.py && \
    echo "Demo app" > /home/user/app/current/README.md && \
    chmod 0644 /home/user/app/current/app.py && \
    chmod 0644 /home/user/app/current/README.md

# From %environment
RUN chmod 755 /home/user
ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

# From %labels
LABEL Author="Automated build"
LABEL Description="Container for deployment snapshot task with initial state and pytest installed."