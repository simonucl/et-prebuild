# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Metadata from %labels
LABEL Author="example"
LABEL Description="Container for release-scraping task – provides canonical HTML sources and pytest."

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0777 /home/user
RUN mkdir -p /home/user/releases

RUN cat <<'EOF' > /home/user/releases/auth-service.html
<!DOCTYPE html>
<html>
<head><title>Auth Service Releases</title></head>
<body>
    <h1>Auth Service</h1>
    <div class="latest-release">
        <span class="version">v1.8.3</span>
        <span class="released">2023-07-18</span>
    </div>
    <div class="latest-release">
        <span class="version">v1.8.2</span>
        <span class="released">2023-06-02</span>
    </div>
</body>
</html>
EOF

RUN cat <<'EOF' > /home/user/releases/payment-service.html
<!DOCTYPE html>
<html>
<head><title>Payment Service Releases</title></head>
<body>
    <h1>Payment Service</h1>
    <div class="latest-release">
        <span class="version">v3.2.0</span>
        <span class="released">2023-07-20</span>
    </div>
    <div class="latest-release">
        <span class="version">v3.1.4</span>
        <span class="released">2023-05-15</span>
    </div>
</body>
</html>
EOF

RUN cat <<'EOF' > /home/user/releases/notification-service.html
<!DOCTYPE html>
<html>
<head><title>Notification Service Releases</title></head>
<body>
    <h1>Notification Service</h1>
    <div class="latest-release">
        <span class="version">v2.0.5</span>
        <span class="released">2023-07-21</span>
    </div>
    <div class="latest-release">
        <span class="version">v2.0.4</span>
        <span class="released">2023-06-30</span>
    </div>
</body>
</html>
EOF

RUN chmod -R a+r /home/user/releases && chmod 755 /home/user