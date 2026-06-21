FROM ubuntu:22.04

# 1. Install Python tooling and pytest
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        python3-setuptools && \
    pip3 install --no-cache-dir pytest

# 2. Prepare initial filesystem state expected by the tests
RUN mkdir -p /home/user && \
    chmod 0777 /home/user && \
    mkdir -p /home/user/build/bin

# 3. Provide the three fixed build artifacts
RUN printf 'alpha build artifact v1.0\n' > /home/user/build/bin/tool_alpha && \
    printf 'beta build artifact v1.0\n'  > /home/user/build/bin/tool_beta && \
    printf 'gamma build artifact v1.0\n' > /home/user/build/bin/tool_gamma && \
    chmod 0644 /home/user/build/bin/tool_alpha \
               /home/user/build/bin/tool_beta  \
               /home/user/build/bin/tool_gamma

# Environment setup
RUN chmod 755 /home/user
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Labels
LABEL Author="Apptainer Task Setup – ChatGPT"