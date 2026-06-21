FROM ubuntu:22.04

# Author: Container build script
# Description: Starter environment for the user-account data-pipeline task. Includes dataset and pytest.
# Help:
#   This image provides:
#     - The required starting dataset under /home/user/data/users
#     - pytest pre-installed for the autograder
#   No output artefacts are created during build; the workspace starts clean.

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PATH="/home/user/.local/bin:${PATH}"

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/data/users

RUN cat <<'EOF' > /home/user/data/users/alpha.txt
alice,alice@example.com,1001,true
bob,bob@example,1002,TRUE
carol,carol@example.com,1003,false
EOF

RUN cat <<'EOF' > /home/user/data/users/beta.txt
dave,dave@example.com,1004,true
eve,eve@example.com,,true
frank,frank@example.com,1006,TRUE
EOF

RUN cat <<'EOF' > /home/user/data/users/gamma.txt
grace,grace@example.com,1007,false
heidi,heidi@sample.com,1008,true
invalidlinewithoutcommas
EOF

RUN chmod 777 /home/user && \
    chmod 755 /home/user/data && \
    chmod 755 /home/user/data/users && \
    chmod 444 /home/user/data/users/*.txt

LABEL Author="Container build script"
LABEL Description="Starter environment for the user-account data-pipeline task. Includes dataset and pytest."