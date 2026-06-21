FROM ubuntu:22.04

# Help section (as comments):
# This container sets up the initial environment for the
# micro-services backup and asset extraction exercise. Pytest is installed
# for automated grading.

# Labels
LABEL Author="Automated build for backup/asset exercise"
LABEL Description="Container image that provides the initial file system state required for the micro-services backup task."

RUN set -e && \
    echo "Updating apt and installing required packages..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        tar \
        gzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN echo "Installing pytest via pip..." && \
    pip3 install --no-cache-dir --progress-bar off pytest

RUN echo "Creating initial directory tree and files for the exercise..." && \
    mkdir -p /home/user && \
    chmod 0777 /home/user

# Create micro-service source trees
RUN mkdir -p /home/user/projects/microservices/microserviceA && \
    mkdir -p /home/user/projects/microservices/microserviceB && \
    mkdir -p /home/user/projects/microservices/microserviceC

# microserviceA files
RUN cat > /home/user/projects/microservices/microserviceA/app.py <<'EOF'
print('A')
EOF

RUN cat > /home/user/projects/microservices/microserviceA/requirements.txt <<'EOF'
flask==2.0.0
EOF

# microserviceB files
RUN cat > /home/user/projects/microservices/microserviceB/server.js <<'EOF'
console.log('B');
EOF

RUN cat > /home/user/projects/microservices/microserviceB/package.json <<'EOF'
{ "name": "B" }
EOF

# microserviceC files
RUN cat > /home/user/projects/microservices/microserviceC/main.go <<'EOF'
package main
func main(){}
EOF

RUN cat > /home/user/projects/microservices/microserviceC/go.mod <<'EOF'
module C
EOF

# Pre-built asset bundle
RUN echo "Creating assets tarball..." && \
    mkdir -p /home/user/resources && \
    mkdir -p /tmp/assets_dir/images /tmp/assets_dir/css && \
    printf "PNGDATA\n" > /tmp/assets_dir/images/logo.png && \
    printf "body{margin:0}\n" > /tmp/assets_dir/css/style.css && \
    tar -C /tmp/assets_dir -czf /home/user/resources/assets.tar.gz \
        ./images/logo.png \
        ./css/style.css && \
    rm -rf /tmp/assets_dir

# Ensure tree readability and set permissions
RUN chmod -R a+rX /home/user/projects /home/user/resources && \
    chmod 755 /home/user

WORKDIR /home/user