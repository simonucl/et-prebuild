FROM ubuntu:24.04

# trsi: pre-create harbor mount points world-writable so non-root-USER envs can be staged
USER root
RUN mkdir -p /solution /tests /logs && chmod 1777 /solution /tests /logs

WORKDIR /home/user/platform

RUN apt-get update \
    && apt-get install -y --no-install-recommends bash python3 python3-yaml coreutils ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m -s /bin/bash user \
    && mkdir -p /home/user/platform/base

RUN cat > /home/user/platform/base/kustomization.yaml <<'EOF'
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - deployment.yaml
  - service.yaml
  - configmap.yaml
EOF

RUN cat > /home/user/platform/base/deployment.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payments-api
  labels:
    app.kubernetes.io/name: payments-api
    app.kubernetes.io/component: api
spec:
  replicas: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: payments-api
      app.kubernetes.io/component: api
  template:
    metadata:
      labels:
        app.kubernetes.io/name: payments-api
        app.kubernetes.io/component: api
    spec:
      containers:
        - name: api
          image: ghcr.io/acme/payments-api:1.9.0
          imagePullPolicy: IfNotPresent
          ports:
            - name: http
              containerPort: 8080
          env:
            - name: LOG_LEVEL
              value: debug
            - name: FEATURE_FLAG_MOCK_GATEWAY
              value: "true"
          envFrom:
            - configMapRef:
                name: payments-api-config
EOF

RUN cat > /home/user/platform/base/service.yaml <<'EOF'
apiVersion: v1
kind: Service
metadata:
  name: payments-api
  labels:
    app.kubernetes.io/name: payments-api
    app.kubernetes.io/component: api
spec:
  type: ClusterIP
  selector:
    app.kubernetes.io/name: payments-api
    app.kubernetes.io/component: api
  ports:
    - name: http
      port: 80
      targetPort: http
EOF

RUN cat > /home/user/platform/base/configmap.yaml <<'EOF'
apiVersion: v1
kind: ConfigMap
metadata:
  name: payments-api-config
data:
  PAYMENT_PROVIDER: sandbox
  LOG_FORMAT: pretty
  CACHE_TTL_SECONDS: "30"
EOF

RUN chown -R user:user /home/user/platform

USER user
