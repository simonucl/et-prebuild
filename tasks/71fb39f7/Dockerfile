FROM ubuntu:22.04

# ------------------------------------------------------------------
# Basic utilities and Python tooling
# ------------------------------------------------------------------
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        rsync && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the test-runner
RUN pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Prepare the golden source tree in /home/user/source_env
# ------------------------------------------------------------------
RUN mkdir -p /home/user/source_env/data

# app.py
RUN cat > /home/user/source_env/app.py <<'EOF'
print("Hello QA")
EOF

# README.md
RUN echo 'Example project for rsync test' > /home/user/source_env/README.md

# requirements.txt
RUN cat > /home/user/source_env/requirements.txt <<'EOF'
flask==2.0.2
pytest==7.4.0
EOF

# data/sample.json
RUN echo '{ "value": 42 }' > /home/user/source_env/data/sample.json

# ------------------------------------------------------------------
# Ensure the student can create new items under /home/user
# ------------------------------------------------------------------
RUN chmod 0777 /home/user

ENV HOME=/home/user

WORKDIR /home/user

CMD ["/bin/bash"]