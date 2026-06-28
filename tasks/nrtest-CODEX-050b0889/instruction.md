# Production Kustomize Overlay

You are preparing the production Kubernetes release manifests for the payments API.

The existing base lives at:

`/home/user/platform/base`

Do not modify any file under `base/`. Create a new Kustomize-style overlay under:

`/home/user/platform/overlays/prod`

The overlay must represent this production release:

- Namespace: `payments-prod`
- Common labels on every generated or patched object:
  - `environment: prod`
  - `app.kubernetes.io/part-of: checkout-platform`
- Deployment `payments-api`:
  - `replicas: 4`
  - image tag `ghcr.io/acme/payments-api:2.4.7`
  - container `api` keeps port name `http`
  - `LOG_LEVEL` is `info`
  - `FEATURE_FLAG_MOCK_GATEWAY` is `"false"`
  - add `envFrom` for secret `payments-api-secrets` while keeping the existing config map reference
  - requests: `cpu: 250m`, `memory: 256Mi`
  - limits: `cpu: 1000m`, `memory: 512Mi`
  - readiness probe: HTTP GET `/ready` on port `http`, `initialDelaySeconds: 5`, `periodSeconds: 10`
  - liveness probe: HTTP GET `/healthz` on port `http`, `initialDelaySeconds: 15`, `periodSeconds: 20`
  - container security context: `allowPrivilegeEscalation: false`, `readOnlyRootFilesystem: true`, `runAsNonRoot: true`, and drop capability `ALL`
  - pod security context: `fsGroup: 2000`
  - prefer not scheduling two matching pods on the same node by adding a pod anti-affinity preference with weight `100`, topology key `kubernetes.io/hostname`, and selector `app.kubernetes.io/name In [payments-api]`
- Service `payments-api`:
  - still targets the container port named `http`
  - expose service port `443`
  - port name `https`
  - `appProtocol: https`
- Merge production ConfigMap values into `payments-api-config`:
  - `PAYMENT_PROVIDER=stripe`
  - `LOG_FORMAT=json`
  - `CACHE_TTL_SECONDS=300`
- Generate secret `payments-api-secrets` with:
  - `STRIPE_API_BASE=https://api.stripe.com`
  - `WEBHOOK_TOLERANCE_SECONDS=300`
- Disable generated name suffix hashes so the ConfigMap and Secret names remain exactly `payments-api-config` and `payments-api-secrets`.

Create these overlay source files:

- `/home/user/platform/overlays/prod/kustomization.yaml`
- `/home/user/platform/overlays/prod/deployment-prod-patch.yaml`
- `/home/user/platform/overlays/prod/service-prod-patch.yaml`

Also render the final production manifest to:

`/home/user/platform/releases/payments-prod.yaml`

The rendered manifest must contain the production Deployment, Service, ConfigMap, and Secret. It should be valid multi-document YAML and should reflect the overlay result, not the unmodified base.
