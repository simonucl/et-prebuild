FROM ubuntu:22.04

# Author: integration-prep
# Description: Container image for SSH-key generation task. Provides a clean
#              environment where no key material exists yet and pytest is
#              available for automated grading.

# Help:
# This image is prepared for an exercise where the learner must create an
# Ed25519 key-pair, register it for password-less SSH, and log metadata.
# The container intentionally starts without any ~/.ssh material so that
# the learner can generate it from scratch. Pytest is pre-installed for
# automated test execution.

# Update package lists and install required software
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        openssh-client \
        ca-certificates \
        locales && \
    locale-gen en_US.UTF-8 && \
    pip3 install --no-cache-dir pytest && \
    useradd --create-home --shell /bin/bash user && \
    chmod 755 /home/user && \
    chown -R user:user /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin

CMD ["/bin/bash"]