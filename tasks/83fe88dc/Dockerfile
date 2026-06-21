FROM ubuntu:22.04

# Maintainer="Apptainer Task Builder"
# Description="Environment for ETL curl exercise with pytest pre-installed."

ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

RUN set -e && \
    echo "Updating apt index and installing required packages..." && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN echo "Installing pytest via pip..." && \
    python3 -m pip install --no-cache-dir pytest

RUN echo "Creating directory structure under /home/user..." && \
    mkdir -p /home/user/mock_api && \
    mkdir -p /home/user/data

RUN echo "Seeding mock API payload..." && \
    cat << 'EOF' > /home/user/mock_api/posts.json
{
  "posts": [
    { "id": 101, "title": "Build pipelines" },
    { "id": 102, "title": "Test ETL" },
    { "id": 103, "title": "Deploy to prod" }
  ]
}
EOF

RUN echo "Setting permissions..." && \
    chmod 755 /home/user && \
    chmod 755 /home/user/mock_api && \
    chmod 755 /home/user/data && \
    chmod 644 /home/user/mock_api/posts.json

CMD ["/bin/bash"]