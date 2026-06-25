#!/bin/bash
set -euo pipefail

python3 - <<'PY'
import gzip
import hashlib
import io
import os
import tarfile
from datetime import datetime, timezone

repo = "/app/repo"
chart_path = os.path.join(repo, "charts", "edge-router-0.8.3.tgz")
os.makedirs(os.path.dirname(chart_path), exist_ok=True)

files = [
    ("edge-router/Chart.yaml", """apiVersion: v2
name: edge-router
description: Edge ingress routing rules for Acme clusters.
type: application
version: 0.8.3
appVersion: "1.9.4"
kubeVersion: ">=1.27.0-0"
maintainers:
  - name: platform-release
    email: platform-release@acme.invalid
"""),
    ("edge-router/values.yaml", """replicaCount: 3
image:
  repository: ghcr.io/acme/edge-router
  tag: "1.9.4"
  pullPolicy: IfNotPresent
service:
  type: ClusterIP
  port: 8080
"""),
    ("edge-router/templates/_helpers.tpl", """{{- define "edge-router.name" -}}
edge-router
{{- end -}}
{{- define "edge-router.fullname" -}}
{{ include "edge-router.name" . }}
{{- end -}}
"""),
    ("edge-router/templates/deployment.yaml", """apiVersion: apps/v1
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
"""),
    ("edge-router/templates/service.yaml", """apiVersion: v1
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
"""),
]

mtime = int(datetime(2024, 4, 3, 12, 0, 0, tzinfo=timezone.utc).timestamp())
tar_buf = io.BytesIO()
with tarfile.open(fileobj=tar_buf, mode="w", format=tarfile.USTAR_FORMAT) as tf:
    for name, text in files:
        data = text.encode("utf-8")
        info = tarfile.TarInfo(name)
        info.size = len(data)
        info.mtime = mtime
        info.mode = 0o644
        info.uid = 0
        info.gid = 0
        info.uname = ""
        info.gname = ""
        tf.addfile(info, io.BytesIO(data))

gz_buf = io.BytesIO()
with gzip.GzipFile(filename="", mode="wb", fileobj=gz_buf, compresslevel=9, mtime=0) as gz:
    gz.write(tar_buf.getvalue())

chart_bytes = gz_buf.getvalue()
with open(chart_path, "wb") as f:
    f.write(chart_bytes)

chart_digest = hashlib.sha256(chart_bytes).hexdigest()
index = f"""apiVersion: v1
entries:
  edge-router:
    - apiVersion: v2
      appVersion: "1.9.4"
      created: "2026-06-25T00:00:00Z"
      description: Edge ingress routing rules for Acme clusters.
      digest: {chart_digest}
      kubeVersion: ">=1.27.0-0"
      maintainers:
        - email: platform-release@acme.invalid
          name: platform-release
      name: edge-router
      type: application
      urls:
        - charts/edge-router-0.8.3.tgz
      version: 0.8.3
generated: "2026-06-25T00:00:00Z"
"""
index_path = os.path.join(repo, "index.yaml")
with open(index_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(index)

index_digest = hashlib.sha256(index.encode("utf-8")).hexdigest()
with open(os.path.join(repo, "SHA256SUMS"), "w", encoding="utf-8", newline="\n") as f:
    f.write(f"{chart_digest}  charts/edge-router-0.8.3.tgz\n")
    f.write(f"{index_digest}  index.yaml\n")

stale = os.path.join(repo, "charts", "edge-router-0.8.2.tgz")
if os.path.exists(stale):
    os.unlink(stale)
PY
