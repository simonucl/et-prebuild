FROM ubuntu:22.04

# Help:
# This container supplies:
#   • pytest (pre-installed)
#   • An offline wheel for sqlparse 0.4.4 in /home/user/prebuilt_wheels
# The wheel is intended for user-level installation via:
#   pip install --user --no-index --find-links=/home/user/prebuilt_wheels sqlparse==0.4.4

ENV HOME=/home/user

RUN set -e \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        python3-wheel \
        ca-certificates \
        wget \
    && python3 -m pip install --no-cache-dir pytest \
    && mkdir -p /home/user/prebuilt_wheels \
    && python3 -m pip download --no-deps --only-binary=:all: \
        --dest /home/user/prebuilt_wheels \
        sqlparse==0.4.4 \
    && find /home/user/prebuilt_wheels -type f ! -name 'sqlparse-0.4.4-py3-none-any.whl' -delete \
    && chmod -R a+rX /home/user \
    && chmod 755 /home/user

CMD ["/bin/bash"]