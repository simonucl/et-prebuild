FROM ubuntu:22.04

# Labels
LABEL Author="Auto-generated setup for CICD build–release exercise"

# Environment variables
ENV LC_ALL=C.UTF-8

# Update package lists and install Python + pip
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Set up the initial filesystem expected by the assignment tests
# Create directories
RUN mkdir -p /home/user/cicd/builds && \
    chmod 755 /home/user && \
    chmod 755 /home/user/cicd && \
    chmod 755 /home/user/cicd/builds

# Create the three placeholder JAR artifacts with the required payload
RUN echo 'dummy jar payload v1.2.3' > /home/user/cicd/builds/artifact-1.2.3.jar && \
    echo 'dummy jar payload v1.2.4' > /home/user/cicd/builds/artifact-1.2.4.jar && \
    echo 'dummy jar payload v1.3.0' > /home/user/cicd/builds/artifact-1.3.0.jar

# Guarantee each file ends with a single trailing newline
RUN sed -i -e '$a\' /home/user/cicd/builds/artifact-1.2.3.jar && \
    sed -i -e '$a\' /home/user/cicd/builds/artifact-1.2.4.jar && \
    sed -i -e '$a\' /home/user/cicd/builds/artifact-1.3.0.jar && \
    chmod 644 /home/user/cicd/builds/artifact-1*.jar

# Clean up apt caches to keep the image small
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*