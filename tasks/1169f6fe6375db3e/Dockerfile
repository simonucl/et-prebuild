FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
  && apt-get install -y --no-install-recommends bash ca-certificates nodejs npm coreutils \
  && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash user
WORKDIR /home/user

RUN set -eux; \
  mkdir -p /home/user/work/route-lens/bin \
    /home/user/work/route-lens/lib \
    /home/user/work/route-lens/test/fixtures \
    /home/user/work/route-lens/docs/internal \
    /home/user/work/route-lens/tmp; \
  printf '%s\n' \
    '{"name":"route-lens-internal","version":"2.0.9","private":true,"description":"internal route inspection utility","main":"lib/index.js","scripts":{"test":"node test/smoke.js"}}' \
    > /home/user/work/route-lens/package.json; \
  printf '%s\n' \
    '#!/usr/bin/env node' \
    'const { summarizeRoutes } = require("../lib/index");' \
    '' \
    'const routes = process.argv.slice(2);' \
    'for (const line of summarizeRoutes(routes)) {' \
    '  console.log(line);' \
    '}' \
    > /home/user/work/route-lens/bin/route-lens.js; \
  printf '%s\n' \
    'const { normalizeRoute } = require("./normalize");' \
    '' \
    'function summarizeRoutes(routes) {' \
    '  if (routes.length === 0) {' \
    '    return ["route-lens: no routes supplied"];' \
    '  }' \
    '  return routes.map((route, idx) => `${idx + 1}. ${normalizeRoute(route)}`);' \
    '}' \
    '' \
    'module.exports = { summarizeRoutes };' \
    > /home/user/work/route-lens/lib/index.js; \
  printf '%s\n' \
    'function normalizeRoute(route) {' \
    '  return String(route || "/").replace(/\/+/g, "/").replace(/\/$/, "") || "/";' \
    '}' \
    '' \
    'module.exports = { normalizeRoute };' \
    > /home/user/work/route-lens/lib/normalize.js; \
  printf '%s\n' \
    '# route-lens' \
    '' \
    'Small CLI for normalizing and listing route paths before edge-router deploys.' \
    > /home/user/work/route-lens/README.md; \
  printf '%s\n' \
    'MIT' \
    > /home/user/work/route-lens/LICENSE; \
  printf '%s\n' \
    'const { summarizeRoutes } = require("../lib");' \
    'if (summarizeRoutes(["//api//v1/"])[0] !== "1. /api/v1") {' \
    '  throw new Error("normalization failed");' \
    '}' \
    > /home/user/work/route-lens/test/smoke.js; \
  printf '%s\n' \
    'Internal release note draft. This file must not be published in the npm tarball.' \
    > /home/user/work/route-lens/docs/internal/release-notes.md; \
  printf '%s\n' \
    'scratch output from local dry-runs' \
    > /home/user/work/route-lens/tmp/debug.log; \
  chmod 0644 /home/user/work/route-lens/bin/route-lens.js; \
  chown -R user:user /home/user/work

USER user
WORKDIR /home/user
