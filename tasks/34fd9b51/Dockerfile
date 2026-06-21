FROM ubuntu:22.04

# Labels
LABEL Author="ExampleAuthor"
LABEL Description="Container with sentiment140 mini-dataset and pytest pre-installed."

# System preparation
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        tzdata \
        gnupg \
        tar && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create directory structure
RUN mkdir -p /home/user/datasets/sentiment140

# train_part1.txt
RUN cat > /home/user/datasets/sentiment140/train_part1.txt <<'EOF'
I love this movie	positive
It was great!	positive
EOF

# train_part2.txt
RUN cat > /home/user/datasets/sentiment140/train_part2.txt <<'EOF'
I hate this movie	negative
It was terrible!	negative
EOF

# train_part3.txt
RUN cat > /home/user/datasets/sentiment140/train_part3.txt <<'EOF'
It was okay	neutral
Not bad, not good	neutral
EOF

# Set permissions
RUN chmod 0777 /home/user/datasets /home/user/datasets/sentiment140 && \
    chmod 0644 /home/user/datasets/sentiment140/train_part*.txt

# Environment settings
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN chmod 755 /home/user

CMD ["/bin/bash"]