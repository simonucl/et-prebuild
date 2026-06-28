#!/bin/bash
set -u

ROOT="${TASK_ROOT:-}"
REWARD="${ROOT}/logs/verifier/reward.txt"
mkdir -p "$(dirname "$REWARD")"

python3 - <<'PY'
import base64
import pathlib
import sys

try:
    import yaml
except Exception as exc:
    print(f"failed to import yaml: {exc}", file=sys.stderr)
    sys.exit(1)

root = pathlib.Path(__import__("os").environ.get("TASK_ROOT") or "/")
platform = root / "home/user/platform"
base = platform / "base"
overlay = platform / "overlays/prod"
release = platform / "releases/payments-prod.yaml"

def fail(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)

def load_yaml(path):
    try:
        with path.open() as f:
            return yaml.safe_load(f)
    except Exception as exc:
        fail(f"cannot parse {path}: {exc}")

def load_docs(path):
    try:
        with path.open() as f:
            return [doc for doc in yaml.safe_load_all(f) if doc is not None]
    except Exception as exc:
        fail(f"cannot parse rendered manifest {path}: {exc}")

def labels_ok(obj):
    labels = obj.get("metadata", {}).get("labels", {})
    return (
        labels.get("environment") == "prod"
        and labels.get("app.kubernetes.io/part-of") == "checkout-platform"
    )

def container_from(dep):
    containers = dep["spec"]["template"]["spec"]["containers"]
    matches = [c for c in containers if c.get("name") == "api"]
    if len(matches) != 1:
        fail("rendered Deployment must contain exactly one api container")
    return matches[0]

required_files = [
    overlay / "kustomization.yaml",
    overlay / "deployment-prod-patch.yaml",
    overlay / "service-prod-patch.yaml",
    release,
]
for path in required_files:
    if not path.is_file():
        fail(f"missing required file: {path}")

base_dep = load_yaml(base / "deployment.yaml")
if base_dep["spec"].get("replicas") != 1:
    fail("base deployment was modified")
if container_from(base_dep).get("image") != "ghcr.io/acme/payments-api:1.9.0":
    fail("base deployment image was modified")

kust = load_yaml(overlay / "kustomization.yaml")
if kust.get("apiVersion") != "kustomize.config.k8s.io/v1beta1" or kust.get("kind") != "Kustomization":
    fail("kustomization.yaml must be a kustomize.config.k8s.io/v1beta1 Kustomization")
if kust.get("resources") != ["../../base"]:
    fail("overlay resources must contain only ../../base")
if kust.get("namespace") != "payments-prod":
    fail("overlay namespace must be payments-prod")
if kust.get("commonLabels", {}) != {
    "environment": "prod",
    "app.kubernetes.io/part-of": "checkout-platform",
}:
    fail("overlay commonLabels are missing or wrong")
if kust.get("generatorOptions", {}).get("disableNameSuffixHash") is not True:
    fail("generated name suffix hashes must be disabled")

def literal_map(items):
    result = {}
    for item in items or []:
        if "=" not in item:
            fail(f"literal is not KEY=VALUE: {item}")
        key, value = item.split("=", 1)
        result[key] = value
    return result

cm_generators = [g for g in kust.get("configMapGenerator", []) if g.get("name") == "payments-api-config"]
if len(cm_generators) != 1 or cm_generators[0].get("behavior") != "merge":
    fail("must merge exactly one payments-api-config ConfigMap generator")
if literal_map(cm_generators[0].get("literals")) != {
    "PAYMENT_PROVIDER": "stripe",
    "LOG_FORMAT": "json",
    "CACHE_TTL_SECONDS": "300",
}:
    fail("ConfigMap generator literals are incorrect")

secret_generators = [g for g in kust.get("secretGenerator", []) if g.get("name") == "payments-api-secrets"]
if len(secret_generators) != 1:
    fail("must generate exactly one payments-api-secrets Secret")
if literal_map(secret_generators[0].get("literals")) != {
    "STRIPE_API_BASE": "https://api.stripe.com",
    "WEBHOOK_TOLERANCE_SECONDS": "300",
}:
    fail("Secret generator literals are incorrect")

images = [img for img in kust.get("images", []) if img.get("name") == "ghcr.io/acme/payments-api"]
if len(images) != 1 or images[0].get("newTag") != "2.4.7":
    fail("image transformer must set ghcr.io/acme/payments-api newTag to 2.4.7")

patch_paths = []
for patch in kust.get("patches", []):
    if isinstance(patch, str):
        patch_paths.append(patch)
    elif isinstance(patch, dict) and "path" in patch:
        patch_paths.append(patch["path"])
patch_paths.extend(kust.get("patchesStrategicMerge", []) or [])
if sorted(patch_paths) != ["deployment-prod-patch.yaml", "service-prod-patch.yaml"]:
    fail("overlay must reference exactly the deployment and service patch files")

dep_patch = load_yaml(overlay / "deployment-prod-patch.yaml")
svc_patch = load_yaml(overlay / "service-prod-patch.yaml")
if dep_patch.get("kind") != "Deployment" or dep_patch.get("metadata", {}).get("name") != "payments-api":
    fail("deployment patch must target Deployment/payments-api")
if svc_patch.get("kind") != "Service" or svc_patch.get("metadata", {}).get("name") != "payments-api":
    fail("service patch must target Service/payments-api")

docs = load_docs(release)
if len(docs) != 4:
    fail("rendered manifest must contain exactly four YAML documents")
by_kind_name = {(d.get("kind"), d.get("metadata", {}).get("name")): d for d in docs}
expected_keys = {
    ("Deployment", "payments-api"),
    ("Service", "payments-api"),
    ("ConfigMap", "payments-api-config"),
    ("Secret", "payments-api-secrets"),
}
if set(by_kind_name) != expected_keys:
    fail("rendered manifest must contain Deployment, Service, ConfigMap, and Secret with expected names")

for doc in docs:
    if doc.get("metadata", {}).get("namespace") != "payments-prod":
        fail(f"{doc.get('kind')} has wrong namespace")
    if not labels_ok(doc):
        fail(f"{doc.get('kind')} is missing required common labels")

dep = by_kind_name[("Deployment", "payments-api")]
if dep["spec"].get("replicas") != 4:
    fail("rendered Deployment replicas must be 4")
container = container_from(dep)
if container.get("image") != "ghcr.io/acme/payments-api:2.4.7":
    fail("rendered Deployment image is wrong")
env = {item.get("name"): item.get("value") for item in container.get("env", [])}
if env != {"LOG_LEVEL": "info", "FEATURE_FLAG_MOCK_GATEWAY": "false"}:
    fail("rendered container env values are wrong")
env_from = container.get("envFrom", [])
if {"configMapRef": {"name": "payments-api-config"}} not in env_from:
    fail("rendered Deployment must keep configMapRef envFrom")
if {"secretRef": {"name": "payments-api-secrets"}} not in env_from:
    fail("rendered Deployment must add secretRef envFrom")
if container.get("resources") != {
    "requests": {"cpu": "250m", "memory": "256Mi"},
    "limits": {"cpu": "1000m", "memory": "512Mi"},
}:
    fail("rendered container resources are wrong")
if container.get("readinessProbe", {}).get("httpGet") != {"path": "/ready", "port": "http"}:
    fail("readinessProbe httpGet is wrong")
if container.get("readinessProbe", {}).get("initialDelaySeconds") != 5 or container.get("readinessProbe", {}).get("periodSeconds") != 10:
    fail("readinessProbe timing is wrong")
if container.get("livenessProbe", {}).get("httpGet") != {"path": "/healthz", "port": "http"}:
    fail("livenessProbe httpGet is wrong")
if container.get("livenessProbe", {}).get("initialDelaySeconds") != 15 or container.get("livenessProbe", {}).get("periodSeconds") != 20:
    fail("livenessProbe timing is wrong")
if container.get("securityContext") != {
    "allowPrivilegeEscalation": False,
    "readOnlyRootFilesystem": True,
    "runAsNonRoot": True,
    "capabilities": {"drop": ["ALL"]},
}:
    fail("container securityContext is wrong")
pod_spec = dep["spec"]["template"]["spec"]
if pod_spec.get("securityContext", {}).get("fsGroup") != 2000:
    fail("pod fsGroup must be 2000")
pref = pod_spec.get("affinity", {}).get("podAntiAffinity", {}).get("preferredDuringSchedulingIgnoredDuringExecution", [])
if len(pref) != 1 or pref[0].get("weight") != 100:
    fail("pod anti-affinity preference is missing or wrong")
term = pref[0].get("podAffinityTerm", {})
if term.get("topologyKey") != "kubernetes.io/hostname":
    fail("pod anti-affinity topologyKey is wrong")
exprs = term.get("labelSelector", {}).get("matchExpressions", [])
if {"key": "app.kubernetes.io/name", "operator": "In", "values": ["payments-api"]} not in exprs:
    fail("pod anti-affinity selector is wrong")

svc = by_kind_name[("Service", "payments-api")]
ports = svc.get("spec", {}).get("ports", [])
if ports != [{"name": "https", "port": 443, "targetPort": "http", "appProtocol": "https"}]:
    fail("rendered Service port must be https:443 targeting http with appProtocol https")

cm = by_kind_name[("ConfigMap", "payments-api-config")]
if cm.get("data") != {"PAYMENT_PROVIDER": "stripe", "LOG_FORMAT": "json", "CACHE_TTL_SECONDS": "300"}:
    fail("rendered ConfigMap data is wrong")

secret = by_kind_name[("Secret", "payments-api-secrets")]
if secret.get("type") != "Opaque":
    fail("rendered Secret type must be Opaque")
decoded = {}
for key, value in (secret.get("data") or {}).items():
    try:
        decoded[key] = base64.b64decode(value).decode()
    except Exception:
        fail(f"Secret data value for {key} is not valid base64")
if decoded != {"STRIPE_API_BASE": "https://api.stripe.com", "WEBHOOK_TOLERANCE_SECONDS": "300"}:
    fail("rendered Secret data is wrong")
PY

if [ $? -eq 0 ]; then
  echo 1 > "$REWARD"
else
  echo 0 > "$REWARD"
fi
