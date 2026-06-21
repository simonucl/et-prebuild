FROM ubuntu:22.04

# Help / metadata
LABEL Author="OpenAI ChatGPT"
LABEL Description="Base image for deployment-script automation task with pytest pre-installed."

RUN set -e && \
    apt-get update && \
    apt-get -y install --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    groupadd -g 1000 user && \
    useradd -m -u 1000 -g 1000 user

RUN set -e && \
    DEPLOY_BASE=/home/user/deployment && \
    mkdir -p "${DEPLOY_BASE}/config/current" && \
    mkdir -p "${DEPLOY_BASE}/config/new" && \
    mkdir -p "${DEPLOY_BASE}/logs" && \
    mkdir -p "${DEPLOY_BASE}/scripts" && \
    echo 'version=1.0' > "${DEPLOY_BASE}/config/current/app.conf" && \
    echo 'version=1.0' > "${DEPLOY_BASE}/config/current/db.conf" && \
    echo 'version=1.0' > "${DEPLOY_BASE}/config/current/cache.conf" && \
    echo 'version=2.0' > "${DEPLOY_BASE}/config/new/app.conf" && \
    echo 'version=2.0' > "${DEPLOY_BASE}/config/new/db.conf" && \
    echo 'version=2.0' > "${DEPLOY_BASE}/config/new/cache.conf" && \
    chown -R 1000:1000 /home/user && \
    chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Run script equivalent
CMD echo "Container for deployment-script exercise. Use bash for an interactive shell."