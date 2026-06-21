FROM ubuntu:22.04

# Install Python and pytest
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create required directory structure
RUN mkdir -p /home/user/logs && \
    mkdir -p /home/user/scripts

# Populate the initial application log
RUN cat << 'EOF' > /home/user/logs/app_2023-08-15.log
[2023-08-15 09:15:23] INFO User 123 logged in
[2023-08-15 09:15:24] DEBUG Cache miss for key 'profile_123'
[2023-08-15 09:15:25] ERROR Payment failed for order 987: insufficient_funds
[2023-08-15 09:15:26] WARN Slow query detected (850ms) on endpoint /api/items
[2023-08-15 09:15:27] INFO HTTP/1.1 200 OK
[2023-08-15 09:15:28] ERROR HTTP/1.1 500 Internal Server Error
[2023-08-15 09:15:29] FATAL OutOfMemoryError: Java heap space
[2023-08-15 09:15:30] INFO User 456 logged out
[2023-08-15 09:15:31] ERROR Payment failed for order 988: card_expired
EOF

# Ensure the student can write to /home/user and its sub-directories
RUN chmod -R a+rwX /home/user

# Labels
LABEL Author="OpenAI-ChatGPT"
LABEL Description="Initial environment for the regex-based log filtering utility task"

WORKDIR /home/user