FROM ubuntu:22.04

# Author Mobile‐CI challenge setup
# Original label command: chmod 755 /home/user

ENV PYTHONIOENCODING=UTF-8
ENV LANG=C.UTF-8

RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip \
 && pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/ci-builds

RUN for d in artifacts android-app cache ios-app shared-lib; do \
        mkdir -p "/home/user/ci-builds/$d"; \
    done

RUN dd if=/dev/zero of=/home/user/ci-builds/artifacts/dummy.bin   bs=1M count=25 \
 && dd if=/dev/zero of=/home/user/ci-builds/android-app/dummy.bin bs=1M count=12 \
 && dd if=/dev/zero of=/home/user/ci-builds/cache/dummy.bin       bs=1M count=10 \
 && dd if=/dev/zero of=/home/user/ci-builds/ios-app/dummy.bin     bs=1M count=8 \
 && dd if=/dev/zero of=/home/user/ci-builds/shared-lib/dummy.bin  bs=1M count=5

RUN chmod -R a+rX /home/user
RUN chmod a+rwx /home/user

RUN apt-get clean && rm -rf /var/lib/apt/lists/*