FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        curl \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/api_source && \
    chmod 0777 /home/user && \
    chmod 0775 /home/user/api_source

RUN cat > /home/user/api_source/dataset_schema.json <<'EOF'
{
  "dataset": "iris",
  "version": "1.0",
  "features": ["sepal_length", "sepal_width", "petal_length", "petal_width"],
  "target": "species",
  "classes": ["setosa", "versicolor", "virginica"]
}
EOF

RUN chmod 0644 /home/user/api_source/dataset_schema.json && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8