FROM ubuntu:22.04

# Help section
# Container for Android build-tools symlink task. Use bash to explore.

ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin

RUN set -e \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
    && pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/build-tools/android/v33 \
    && mkdir -p /home/user/build-tools/android/v34

RUN ln -sfn /home/user/build-tools/android/v33 /home/user/build-tools/android/current

RUN chmod 755 /home/user \
    && chmod 755 /home/user/build-tools \
    && chmod 755 /home/user/build-tools/android \
    && chmod 755 /home/user/build-tools/android/v33 \
    && chmod 755 /home/user/build-tools/android/v34

RUN rm -f /home/user/build-tools/link_update.log || true

RUN apt-get clean && rm -rf /var/lib/apt/lists/*