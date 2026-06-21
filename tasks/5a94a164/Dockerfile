FROM ubuntu:22.04

# Labels
LABEL Author="example@example.com"
LABEL Description="Container for quick baseline timing task – ships mock API JSON files and pytest."

# Environment
ENV PATH=/usr/local/bin:$PATH

# Update APT and install prerequisites
RUN set -e && \
    echo "Updating APT and installing prerequisites..." && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        curl \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest via pip
RUN echo "Installing pytest via pip..." && \
    pip3 install --no-cache-dir pytest

# Create /home/user directory with permissive write access
RUN echo "Creating /home/user directory with permissive write access..." && \
    mkdir -p /home/user && \
    chmod 1777 /home/user

# Set up mock API resources directory
RUN echo "Setting up mock API resources..." && \
    mkdir -p /home/user/mock_api && \
    chmod 755 /home/user/mock_api

# Create users.json
RUN cat >/home/user/mock_api/users.json <<'EOF'
[
  { "id": 1, "name": "Alice", "email": "alice@example.com" },
  { "id": 2, "name": "Bob", "email": "bob@example.com" }
]
EOF

# Create posts.json
RUN cat >/home/user/mock_api/posts.json <<'EOF'
[
  { "id": 1, "title": "Hello World", "body": "First post" },
  { "id": 2, "title": "Another Post", "body": "Second post" }
]
EOF

# Create comments.json
RUN cat >/home/user/mock_api/comments.json <<'EOF'
[
  { "id": 1, "postId": 1, "body": "Nice!" },
  { "id": 2, "postId": 1, "body": "Thanks!" }
]
EOF

# Set permissions on JSON files
RUN chmod 644 /home/user/mock_api/*.json

# Set working directory
WORKDIR /home/user

# Default command
CMD ["/bin/bash"]