FROM ubuntu:22.04

# Labels
LABEL Author="Task Preparer"
LABEL Description="Apptainer image for container-names extraction troubleshooting task"

# Update package lists and install Python + pip
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grading tests
RUN pip3 install --no-cache-dir pytest

# Prepare the required directory structure
RUN mkdir -p /home/user/mock

# Create the snapshot file with the exact expected content
RUN cat > /home/user/mock/docker_ps_output.txt <<'EOT'
CONTAINER ID   IMAGE                   COMMAND                  CREATED         STATUS         PORTS                    NAMES
a1b2c3d4e5f6   company/api-gateway     "docker-entrypoint.sh"   2 days ago      Up 2 days      0.0.0.0:8080->8080/tcp   api-gateway
b2c3d4e5f6a1   company/auth-service    "docker-entrypoint.sh"   2 days ago      Up 2 days      0.0.0.0:8081->8081/tcp   auth-service
c3d4e5f6a1b2   postgres:13-alpine      "docker-entrypoint.sh"   2 days ago      Up 2 days      0.0.0.0:5432->5432/tcp   payments-db
EOT

# Ensure the student (non-root) user can read the snapshot and
# create new files in /home/user
RUN chmod -R 0777 /home/user

# Standard PATH
ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"