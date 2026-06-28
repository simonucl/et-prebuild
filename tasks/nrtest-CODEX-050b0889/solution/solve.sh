#!/bin/bash
set -euo pipefail

ROOT="${TASK_ROOT:-}"
BASE="${ROOT}/home/user/platform"
OVERLAY="$BASE/overlays/prod"
RELEASES="$BASE/releases"

mkdir -p "$OVERLAY" "$RELEASES"

cat > "$OVERLAY/kustomization.yaml" <<'EOF'
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - ../../base
namespace: payments-prod
commonLabels:
  environment: prod
  app.kubernetes.io/part-of: checkout-platform
generatorOptions:
  disableNameSuffixHash: true
configMapGenerator:
  - name: payments-api-config
    behavior: merge
    literals:
      - PAYMENT_PROVIDER=stripe
      - LOG_FORMAT=json
      - CACHE_TTL_SECONDS=300
secretGenerator:
  - name: payments-api-secrets
    literals:
      - STRIPE_API_BASE=https://api.stripe.com
      - WEBHOOK_TOLERANCE_SECONDS=300
images:
  - name: ghcr.io/acme/payments-api
    newTag: 2.4.7
patches:
  - path: deployment-prod-patch.yaml
  - path: service-prod-patch.yaml
EOF

cat > "$OVERLAY/deployment-prod-patch.yaml" <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payments-api
spec:
  replicas: 4
  template:
    spec:
      securityContext:
        fsGroup: 2000
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchExpressions:
                    - key: app.kubernetes.io/name
                      operator: In
                      values:
                        - payments-api
                topologyKey: kubernetes.io/hostname
      containers:
        - name: api
          image: ghcr.io/acme/payments-api:2.4.7
          env:
            - name: LOG_LEVEL
              value: info
            - name: FEATURE_FLAG_MOCK_GATEWAY
              value: "false"
          envFrom:
            - configMapRef:
                name: payments-api-config
            - secretRef:
                name: payments-api-secrets
          resources:
            requests:
              cpu: 250m
              memory: 256Mi
            limits:
              cpu: 1000m
              memory: 512Mi
          readinessProbe:
            httpGet:
              path: /ready
              port: http
            initialDelaySeconds: 5
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /healthz
              port: http
            initialDelaySeconds: 15
            periodSeconds: 20
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            runAsNonRoot: true
            capabilities:
              drop:
                - ALL
EOF

cat > "$OVERLAY/service-prod-patch.yaml" <<'EOF'
apiVersion: v1
kind: Service
metadata:
  name: payments-api
spec:
  ports:
    - name: https
      port: 443
      targetPort: http
      appProtocol: https
EOF

cat > "$RELEASES/payments-prod.yaml" <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payments-api
  namespace: payments-prod
  labels:
    app.kubernetes.io/name: payments-api
    app.kubernetes.io/component: api
    environment: prod
    app.kubernetes.io/part-of: checkout-platform
spec:
  replicas: 4
  selector:
    matchLabels:
      app.kubernetes.io/name: payments-api
      app.kubernetes.io/component: api
      environment: prod
      app.kubernetes.io/part-of: checkout-platform
  template:
    metadata:
      labels:
        app.kubernetes.io/name: payments-api
        app.kubernetes.io/component: api
        environment: prod
        app.kubernetes.io/part-of: checkout-platform
    spec:
      securityContext:
        fsGroup: 2000
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchExpressions:
                    - key: app.kubernetes.io/name
                      operator: In
                      values:
                        - payments-api
                topologyKey: kubernetes.io/hostname
      containers:
        - name: api
          image: ghcr.io/acme/payments-api:2.4.7
          imagePullPolicy: IfNotPresent
          ports:
            - name: http
              containerPort: 8080
          env:
            - name: LOG_LEVEL
              value: info
            - name: FEATURE_FLAG_MOCK_GATEWAY
              value: "false"
          envFrom:
            - configMapRef:
                name: payments-api-config
            - secretRef:
                name: payments-api-secrets
          resources:
            requests:
              cpu: 250m
              memory: 256Mi
            limits:
              cpu: 1000m
              memory: 512Mi
          readinessProbe:
            httpGet:
              path: /ready
              port: http
            initialDelaySeconds: 5
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /healthz
              port: http
            initialDelaySeconds: 15
            periodSeconds: 20
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            runAsNonRoot: true
            capabilities:
              drop:
                - ALL
---
apiVersion: v1
kind: Service
metadata:
  name: payments-api
  namespace: payments-prod
  labels:
    app.kubernetes.io/name: payments-api
    app.kubernetes.io/component: api
    environment: prod
    app.kubernetes.io/part-of: checkout-platform
spec:
  type: ClusterIP
  selector:
    app.kubernetes.io/name: payments-api
    app.kubernetes.io/component: api
    environment: prod
    app.kubernetes.io/part-of: checkout-platform
  ports:
    - name: https
      port: 443
      targetPort: http
      appProtocol: https
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: payments-api-config
  namespace: payments-prod
  labels:
    environment: prod
    app.kubernetes.io/part-of: checkout-platform
data:
  PAYMENT_PROVIDER: stripe
  LOG_FORMAT: json
  CACHE_TTL_SECONDS: "300"
---
apiVersion: v1
kind: Secret
metadata:
  name: payments-api-secrets
  namespace: payments-prod
  labels:
    environment: prod
    app.kubernetes.io/part-of: checkout-platform
type: Opaque
data:
  STRIPE_API_BASE: aHR0cHM6Ly9hcGkuc3RyaXBlLmNvbQ==
  WEBHOOK_TOLERANCE_SECONDS: MzAw
EOF
