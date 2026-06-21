FROM ubuntu:22.04

# Help section comments (no %help in original)

ENV PATH="/usr/local/bin:${PATH}"
ENV HOME="/home/user"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/projects/widget-service/config/deployments

RUN cat > /home/user/projects/widget-service/config/deployments/prod.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: widget-service
spec:
  replicas: 3
  template:
    metadata:
      labels:
        app: widget
    spec:
      containers:
        - name: widget
          image: registry.example.com/widget-service:1.4.2
          env:
            - name: NODE_ENV
              value: "production"
          ports:
            - containerPort: 8080
EOF

RUN cat > /home/user/projects/widget-service/config/settings.toml <<'EOF'
[service]
name = "widget-service"
version = "1.4.2"

[logging]
level = "info"
file = "/var/log/widget-service.log"
EOF

RUN chmod -R 777 /home/user/projects/widget-service && \
    chmod 777 /home/user /home/user/projects || true && \
    chmod 755 /home/user

CMD ["/bin/bash"]