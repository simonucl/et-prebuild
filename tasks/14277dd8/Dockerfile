FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        zip \
        unzip \
        tar \
        gzip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/build_artifacts/libs && \
    mkdir -p /home/user/build_artifacts/configs

RUN printf 'Alpha library binary mock v1.0\n' > /home/user/build_artifacts/libs/libalpha.txt && \
    printf 'Beta library binary mock v1.0\n'  > /home/user/build_artifacts/libs/libbeta.txt

RUN printf '[app]\nname=DemoApp\nversion=1.0.0\n' > /home/user/build_artifacts/configs/app.conf

RUN printf '# Demo Build Artifacts\nThese are mock artifacts for testing.' \
        > /home/user/build_artifacts/README.md

RUN chmod -R a+rX /home/user

RUN chmod 755 /home/user

CMD ["/bin/bash"]