FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Task Generator"
LABEL Description="Container with initial state for Kubernetes manifest symlink update exercise."

# Update package list and install Python & pip
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the validation framework
RUN pip3 install --no-cache-dir pytest

# Create the initial filesystem state required by the exercise
# Ensure /home/user exists
RUN mkdir -p /home/user

# Create the manifests directory
RUN install -d -m 755 /home/user/k8s/manifests

# Create deployment-v1.yaml with required content
RUN printf 'version: v1\n' > /home/user/k8s/manifests/deployment-v1.yaml

# Create deployment-v2.yaml with required content
RUN printf 'version: v2\n' > /home/user/k8s/manifests/deployment-v2.yaml

# Create a placeholder service.yaml (content not validated)
RUN printf 'kind: Service\n' > /home/user/k8s/manifests/service.yaml

# Ensure files have proper permissions (644)
RUN chmod 644 /home/user/k8s/manifests/deployment-v1.yaml \
              /home/user/k8s/manifests/deployment-v2.yaml \
              /home/user/k8s/manifests/service.yaml

# Create the initial symlink 'current' -> deployment-v1.yaml
RUN ln -sfn deployment-v1.yaml /home/user/k8s/manifests/current

# Set proper permissions on home directory
RUN chmod 755 /home/user

# Environment variables
ENV PATH=/usr/bin:$PATH
ENV PYTHONUNBUFFERED=1

# Help information (as comment)
# This container provides the initial filesystem state for the "update the
# symlink" task. The directory /home/user/k8s/manifests/ contains two deployment
# YAML files, a service YAML, and a symbolic link named "current" that initially
# points to deployment-v1.yaml. Pytest is installed so that automated tests can
# verify the initial state before the learner performs any actions.