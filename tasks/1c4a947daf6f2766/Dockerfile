FROM ubuntu:24.04

WORKDIR /home/user

RUN apt-get update && apt-get install -y python3 ca-certificates && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/npm-lab/src/edge-policy/dist \
    /home/user/npm-lab/src/edge-policy/bin \
    /home/user/npm-lab/src/edge-policy/types \
    /home/user/npm-lab/src/edge-policy/test \
    /home/user/npm-lab/registry/@acme/edge-policy/- \
    && printf '%s\n' \
      '{"name":"@acme/edge-policy","version":"1.2.9","description":"draft package metadata","main":"src/index.js","license":"UNLICENSED"}' \
      > /home/user/npm-lab/src/edge-policy/package.json \
    && printf '%s\n' \
      '# Edge Policy' \
      '' \
      'Small offline policy compiler for edge rule bundles.' \
      > /home/user/npm-lab/src/edge-policy/README.md \
    && printf '%s\n' \
      'MIT License' \
      '' \
      'Copyright (c) 2026 Acme' \
      > /home/user/npm-lab/src/edge-policy/LICENSE \
    && printf '%s\n' \
      'export function compilePolicy(input) {' \
      '  return {' \
      '    version: "1.3.0",' \
      '    rules: input.rules.map((rule) => ({ ...rule, enabled: rule.enabled !== false })),' \
      '  };' \
      '}' \
      > /home/user/npm-lab/src/edge-policy/dist/index.js \
    && printf '%s\n' \
      '{"defaults":{"mode":"enforce","logLevel":"info"},"ruleTypes":["header","rate-limit","redirect"]}' \
      > /home/user/npm-lab/src/edge-policy/dist/rules.json \
    && printf '%s\n' \
      '#!/usr/bin/env node' \
      'import { compilePolicy } from "../dist/index.js";' \
      'const payload = JSON.parse(process.argv[2] || "{\"rules\":[]}");' \
      'process.stdout.write(JSON.stringify(compilePolicy(payload)) + "\n");' \
      > /home/user/npm-lab/src/edge-policy/bin/edge-policy.js \
    && chmod 0755 /home/user/npm-lab/src/edge-policy/bin/edge-policy.js \
    && printf '%s\n' \
      'export interface Rule { enabled?: boolean; [key: string]: unknown }' \
      'export declare function compilePolicy(input: { rules: Rule[] }): { version: "1.3.0"; rules: Rule[] };' \
      > /home/user/npm-lab/src/edge-policy/types/index.d.ts \
    && printf '%s\n' 'temporary notes - do not ship' > /home/user/npm-lab/src/edge-policy/notes.tmp \
    && printf '%s\n' 'console.log("draft test");' > /home/user/npm-lab/src/edge-policy/test/compile.test.js \
    && printf '%s\n' 'stale tarball' > /home/user/npm-lab/registry/@acme/edge-policy/-/edge-policy-1.2.9.tgz \
    && printf '%s\n' '{"stale":true}' > /home/user/npm-lab/registry/@acme/edge-policy/index.json \
    && printf '%s\n' '{"stale":true}' > /home/user/npm-lab/registry/@acme/edge-policy/manifest.json
