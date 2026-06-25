# Repair the Offline Helm Chart Repository

You are preparing a static Helm chart repository for an air-gapped deployment.
The chart source is staged at:

`/app/chart-src/edge-router`

The broken repository to replace is staged at:

`/app/repo`

Do not use the network. Replace the stale repository contents with exactly these release files:

- `/app/repo/charts/edge-router-0.8.3.tgz`
- `/app/repo/index.yaml`
- `/app/repo/SHA256SUMS`

The packaged chart archive must be a deterministic gzip-compressed tar archive:

- The gzip stream must use maximum compression, mtime zero, and no stored original filename.
- The tar archive must contain only regular file entries. Do not include directory entries.
- All archive paths must be under the top-level directory `edge-router/`.
- Archive entries must appear in this exact order:
  1. `edge-router/Chart.yaml`
  2. `edge-router/values.yaml`
  3. `edge-router/templates/_helpers.tpl`
  4. `edge-router/templates/deployment.yaml`
  5. `edge-router/templates/service.yaml`
- Do not include `README.md`, `notes.tmp`, `templates/debug.yaml`, editor backups, or any other files.
- Normalize every tar member to mtime `2024-04-03T12:00:00Z`, numeric owner/group `0/0`, empty owner/group names, and mode `0644`.

Package the chart as version `0.8.3` with app version `1.9.4`. The chart metadata inside `edge-router/Chart.yaml` must be:

```yaml
apiVersion: v2
name: edge-router
description: Edge ingress routing rules for Acme clusters.
type: application
version: 0.8.3
appVersion: "1.9.4"
kubeVersion: ">=1.27.0-0"
maintainers:
  - name: platform-release
    email: platform-release@acme.invalid
```

The packaged `edge-router/values.yaml` must set `replicaCount` to `3`, keep the image repository `ghcr.io/acme/edge-router`, set the image tag to `"1.9.4"`, and keep the service as `ClusterIP` on port `8080`.

Write `/app/repo/index.yaml` as a Helm chart repository index for only this chart version. It must use `apiVersion: v1`, list URL `charts/edge-router-0.8.3.tgz`, include the SHA-256 digest of the final chart archive, and use the created/generated timestamp `2026-06-25T00:00:00Z`.

Write `/app/repo/SHA256SUMS` with exactly two lines:

```text
<sha256 of charts/edge-router-0.8.3.tgz>  charts/edge-router-0.8.3.tgz
<sha256 of index.yaml>  index.yaml
```

The repository must not contain stale chart versions or extra files.
