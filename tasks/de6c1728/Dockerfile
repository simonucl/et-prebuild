FROM ubuntu:22.04

# Help: This container provides the initial filesystem state for the
# network-readiness Compose parsing exercise and includes pytest for
# automated grading.

# Author: platform-engineering-task-preparer

#---------------------------------------------------------------------#
# Install Python and pytest                                            #
#---------------------------------------------------------------------#
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

#---------------------------------------------------------------------#
# Prepare initial filesystem state expected by the grader             #
#---------------------------------------------------------------------#
RUN mkdir -p /home/user/microservices

# auth-service.yaml
RUN cat > /home/user/microservices/auth-service.yaml <<'EOF'
services:
  auth:
    container_name: auth-service
    image: auth-service:latest
    ports:
      - "8001:8000"
EOF

# billing-service.yaml
RUN cat > /home/user/microservices/billing-service.yaml <<'EOF'
services:
  billing:
    container_name: billing-service
    image: billing-service:latest
    ports:
      - "8002:8000"
EOF

# notification-service.yaml
RUN cat > /home/user/microservices/notification-service.yaml <<'EOF'
services:
  notification:
    container_name: notification-service
    image: notification-service:latest
    ports:
      - "8003:8000"
EOF

#---------------------------------------------------------------------#
# Permissions so the non-root agent can read everything               #
#---------------------------------------------------------------------#
RUN chmod -R 755 /home/user && \
    chmod 644 /home/user/microservices/*.yaml