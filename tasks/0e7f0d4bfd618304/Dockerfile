FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && apt-get install -y bash python3 tar gzip coreutils && rm -rf /var/lib/apt/lists/*

RUN set -eux; \
    mkdir -p /app/yarn-lab/app /app/yarn-lab/packages/edge-flags/src /app/yarn-lab/packages/policy-table/data /app/yarn-lab/mirror; \
    printf '%s\n' '{"name":"fleet-console","version":"0.1.0","private":true,"dependencies":{"@acme/edge-flags":"1.2.0","@acme/policy-table":"0.5.1"}}' > /app/yarn-lab/app/package.json; \
    printf '%s\n' '{"name":"@acme/edge-flags","version":"1.1.9","description":"draft metadata","main":"src/index.js"}' > /app/yarn-lab/packages/edge-flags/package.json; \
    printf '%s\n' 'export const FLAGS = Object.freeze({"betaRules":true,"auditSink":"spool"});' > /app/yarn-lab/packages/edge-flags/src/index.js; \
    printf '%s\n' '# Edge Flags' '' 'Offline feature flag constants for edge deployments.' > /app/yarn-lab/packages/edge-flags/README.md; \
    printf '%s\n' 'MIT License' '' 'Copyright (c) 2026 Acme' > /app/yarn-lab/packages/edge-flags/LICENSE; \
    printf '%s\n' '{"name":"@acme/policy-table","version":"0.5.0","description":"old metadata","main":"index.js"}' > /app/yarn-lab/packages/policy-table/package.json; \
    printf '%s\n' 'import { FLAGS } from "@acme/edge-flags";' 'export function policyTable() {' '  return { flags: FLAGS, defaults: { mode: "enforce", sampleRate: 1 } };' '}' > /app/yarn-lab/packages/policy-table/index.js; \
    printf '%s\n' '{"mode":"enforce","sampleRate":1,"outputs":["json","syslog"]}' > /app/yarn-lab/packages/policy-table/data/defaults.json; \
    printf '%s\n' '# stale lock' > /app/yarn-lab/yarn.lock; \
    printf '%s\n' 'yarn-offline-mirror "./old-cache"' > /app/yarn-lab/.yarnrc; \
    printf '%s\n' 'stale tarball' > /app/yarn-lab/mirror/@acme-edge-flags-1.1.9.tgz; \
    printf '%s\n' 'debug' > /app/yarn-lab/mirror/debug.tmp
