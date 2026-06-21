FROM ubuntu:22.04

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        git \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user

WORKDIR /home/user/demo_repo

RUN git init -q && \
    mkdir -p scripts src && \
    printf "Demo repository for testing.\n" > README.md && \
    printf "#!/usr/bin/env bash\n\necho \"Running\"\n" > scripts/run.sh && \
    chmod +x scripts/run.sh

RUN cat > src/main.py <<'PY'
def main():
    print("Hello World")


if __name__ == "__main__":
    main()
PY

RUN git config user.email "builder@example.com" && \
    git config user.name "Builder" && \
    git add README.md scripts/run.sh src/main.py && \
    git commit -qm "Initial commit" && \
    chmod -R a+rX /home/user/demo_repo

ENV LC_ALL=C.UTF-8
ENV PATH=$PATH:/usr/local/bin

WORKDIR /home/user