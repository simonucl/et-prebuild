FROM python:3.12-slim-bookworm

WORKDIR /app

RUN <<'EOF'
set -eu

mkdir -p /app/chart-src/edge-router/templates /app/repo/charts

cat > /app/chart-src/edge-router/Chart.yaml <<'CHART'
apiVersion: v2
name: edge-router
description: Edge ingress routing rules for Acme clusters.
type: application
version: 0.8.2
appVersion: "1.9.3"
kubeVersion: ">=1.26.0-0"
maintainers:
  - name: platform-release
    email: platform-release@acme.invalid
CHART

cat > /app/chart-src/edge-router/values.yaml <<'VALUES'
replicaCount: 2
image:
  repository: ghcr.io/acme/edge-router
  tag: latest
  pullPolicy: IfNotPresent
service:
  type: ClusterIP
  port: 8080
VALUES

cat > /app/chart-src/edge-router/templates/_helpers.tpl <<'HELPERS'
{{- define "edge-router.name" -}}
edge-router
{{- end -}}
{{- define "edge-router.fullname" -}}
{{ include "edge-router.name" . }}
{{- end -}}
HELPERS

cat > /app/chart-src/edge-router/templates/deployment.yaml <<'DEPLOY'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "edge-router.fullname" . }}
  labels:
    app.kubernetes.io/name: {{ include "edge-router.name" . }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app.kubernetes.io/name: {{ include "edge-router.name" . }}
  template:
    metadata:
      labels:
        app.kubernetes.io/name: {{ include "edge-router.name" . }}
    spec:
      containers:
        - name: edge-router
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - name: http
              containerPort: {{ .Values.service.port }}
DEPLOY

cat > /app/chart-src/edge-router/templates/service.yaml <<'SERVICE'
apiVersion: v1
kind: Service
metadata:
  name: {{ include "edge-router.fullname" . }}
  labels:
    app.kubernetes.io/name: {{ include "edge-router.name" . }}
spec:
  type: {{ .Values.service.type }}
  ports:
    - name: http
      port: {{ .Values.service.port }}
      targetPort: http
  selector:
    app.kubernetes.io/name: {{ include "edge-router.name" . }}
SERVICE

cat > /app/chart-src/edge-router/README.md <<'README'
# edge-router

Internal staging notes. This file is not part of the release package.
README

cat > /app/chart-src/edge-router/notes.tmp <<'TMP'
delete before release
TMP

cat > /app/chart-src/edge-router/templates/debug.yaml <<'DEBUG'
apiVersion: v1
kind: ConfigMap
metadata:
  name: debug-only
DEBUG

cat > /app/repo/index.yaml <<'INDEX'
apiVersion: v1
entries: {}
generated: "2025-01-01T00:00:00Z"
INDEX

printf 'stale artifact\n' > /app/repo/charts/edge-router-0.8.2.tgz
printf '0000000000000000000000000000000000000000000000000000000000000000  charts/edge-router-0.8.2.tgz\n' > /app/repo/SHA256SUMS

chmod -R a+rX /app/chart-src /app/repo
EOF
