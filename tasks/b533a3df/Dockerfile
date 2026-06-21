FROM ubuntu:22.04

# Help: Container for the "dataset freeze & checksum" exercise.
# The initial raw dataset is located in /home/user/ml_data/raw.
# Pytest is installed so the grading harness can verify the initial state.

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare the initial filesystem state expected by the exercise
# Dataset directory
RUN mkdir -p /home/user/ml_data/raw

# images_train.csv
RUN cat > /home/user/ml_data/raw/images_train.csv <<'EOF'
id,label
1,cat
2,dog
EOF

# images_val.csv
RUN cat > /home/user/ml_data/raw/images_val.csv <<'EOF'
id,label
3,cat
4,dog
EOF

# labels.json
RUN cat > /home/user/ml_data/raw/labels.json <<'EOF'
{"cat": 0, "dog": 1}
EOF

# Make sure everything is readable by the unprivileged runtime user
RUN chmod -R a+rX /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /home/user