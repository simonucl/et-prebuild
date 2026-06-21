# Author: ChatGPT
# Description: Environment for chat frequency task – provides raw dataset and pytest.
FROM ubuntu:22.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/datasets
RUN chmod 0777 /home/user && chmod 0777 /home/user/datasets

RUN cat > /home/user/datasets/chat_samples.txt <<'EOF'
Hello world, hello AI!
The AI world is vast.
Machine learning fuels the AI revolution.
Hello again, machine learning world.
AI and machine learning are related fields.
World of hello messages.
AI says hello to the world.
Learning about machine intelligence.
EOF

RUN chmod 0644 /home/user/datasets/chat_samples.txt
RUN chmod 755 /home/user

ENV PYTHONIOENCODING=UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Runscript equivalent
CMD echo "Container for the Chat Samples frequency task." && \
    echo "Invoke an interactive shell with: docker run -it <image> /bin/bash"