FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && apt-get install -y bash python3 tar gzip coreutils findutils && rm -rf /var/lib/apt/lists/*

RUN set -eux; \
  mkdir -p /app/collection-src/acme/edge_ops/plugins/modules; \
  mkdir -p /app/collection-src/acme/edge_ops/plugins/module_utils; \
  mkdir -p /app/collection-src/acme/edge_ops/roles/edge_agent/tasks; \
  mkdir -p /app/collection-src/acme/edge_ops/docs; \
  mkdir -p /app/collection-src/acme/edge_ops/tests /app/galaxy/artifacts /app/galaxy/tmp; \
  printf '%s\n' \
    'namespace: acme' \
    'name: edge_ops' \
    'version: 1.2.3' \
    'readme: README.md' \
    'authors:' \
    '  - Acme Platform <platform@acme.invalid>' \
    'description: Offline automation helpers for Acme edge gateways.' \
    'license_file: LICENSE' \
    'tags:' \
    '  - edge' \
    '  - offline' \
    '  - automation' \
    'dependencies: {}' \
    'repository: https://git.example.invalid/acme/edge-ops' \
    'documentation: https://docs.example.invalid/acme/edge-ops' \
    'homepage: https://example.invalid/acme/edge-ops' \
    'issues: https://git.example.invalid/acme/edge-ops/issues' \
    > /app/collection-src/acme/edge_ops/galaxy.yml; \
  printf '%s\n' \
    '# Acme Edge Ops' \
    '' \
    'Offline Ansible collection for edge gateway diagnostics.' \
    > /app/collection-src/acme/edge_ops/README.md; \
  printf '%s\n' \
    'Apache License' \
    'Version 2.0, January 2004' \
    'https://www.apache.org/licenses/' \
    > /app/collection-src/acme/edge_ops/LICENSE; \
  printf '%s\n' \
    '# Usage' \
    '' \
    'Run acme.edge_ops.edge_status to collect local edge health facts.' \
    > /app/collection-src/acme/edge_ops/docs/usage.md; \
  printf '%s\n' \
    'from __future__ import annotations' \
    '' \
    'def normalize_status(payload):' \
    '    return {' \
    '        "node": payload.get("node", "unknown"),' \
    '        "healthy": bool(payload.get("healthy")),' \
    '        "services": sorted(payload.get("services", [])),' \
    '    }' \
    > /app/collection-src/acme/edge_ops/plugins/module_utils/client.py; \
  printf '%s\n' \
    '#!/usr/bin/python' \
    'from __future__ import annotations' \
    '' \
    'from ansible.module_utils.basic import AnsibleModule' \
    'from ansible_collections.acme.edge_ops.plugins.module_utils.client import normalize_status' \
    '' \
    'def main():' \
    '    module = AnsibleModule(argument_spec={"node": {"type": "str", "required": True}})' \
    '    result = normalize_status({"node": module.params["node"], "healthy": True, "services": ["agent", "proxy"]})' \
    '    module.exit_json(changed=False, edge_status=result)' \
    '' \
    'if __name__ == "__main__":' \
    '    main()' \
    > /app/collection-src/acme/edge_ops/plugins/modules/edge_status.py; \
  printf '%s\n' \
    '---' \
    '- name: ensure edge agent directory exists' \
    '  ansible.builtin.file:' \
    '    path: /var/lib/acme-edge' \
    '    state: directory' \
    '    mode: "0755"' \
    > /app/collection-src/acme/edge_ops/roles/edge_agent/tasks/main.yml; \
  printf '%s\n' 'scratch data that must not be packaged' > /app/collection-src/acme/edge_ops/tests/fixture.tmp; \
  printf '%s\n' 'stale artifact' > /app/galaxy/artifacts/acme-edge_ops-1.2.2.tar.gz; \
  printf '%s\n' '{"stale":true}' > /app/galaxy/index.json; \
  printf '%s\n' 'temporary output' > /app/galaxy/tmp/build.log
