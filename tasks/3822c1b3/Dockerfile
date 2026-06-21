FROM ubuntu:22.04

# From %help and %runscript (converted to comments)
# Container for the artifact-manager task.
# Run your solution inside the container shell.

RUN set -e && \
    echo "Updating APT and installing Python tooling..." && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN echo "Installing pytest..." && \
    pip3 install --no-cache-dir pytest

RUN echo "Creating initial repository layout..." && \
    mkdir -p /home/user/repos/stable && \
    touch /home/user/repos/stable/libbar_2.5.1_amd64.deb && \
    touch /home/user/repos/stable/libfoo_1.0.0_amd64.deb && \
    chmod 644 /home/user/repos/stable/libbar_2.5.1_amd64.deb && \
    chmod 644 /home/user/repos/stable/libfoo_1.0.0_amd64.deb && \
    chmod -R a+rX /home/user && \
    chmod 777 /home/user

# From %environment (chmod must be RUN, PATH is ENV)
RUN chmod 755 /home/user
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"