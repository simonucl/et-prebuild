FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends bash ca-certificates coreutils jq nodejs npm python3 tar gzip \
    && rm -rf /var/lib/apt/lists/*

RUN <<'SETUP'
set -e
useradd -m -s /bin/bash user
mkdir -p /home/user/npm-lab/widget-kit/src /home/user/npm-lab/widget-kit/scripts /home/user/npm-lab/handoff
cat > /home/user/npm-lab/widget-kit/package.json <<'EOF'
{"name":"@acme/widget-kit","version":"1.6.4","description":"Offline widget rendering helpers","type":"module","main":"dist/index.cjs","module":"dist/index.mjs","types":"dist/index.d.ts","bin":{"widget-render":"dist/cli.cjs"},"files":["dist/","README.md","LICENSE"],"scripts":{"prepack":"node scripts/build.mjs"}}
EOF
cat > /home/user/npm-lab/widget-kit/README.md <<'EOF'
# Widget Kit

Offline helpers for rendering short widget labels in release tests.
EOF
cat > /home/user/npm-lab/widget-kit/LICENSE <<'EOF'
Proprietary test fixture
EOF
cat > /home/user/npm-lab/widget-kit/src/index.js <<'EOF'
export function renderWidget(name) {
  return `widget:${name.trim().toLowerCase()}`;
}
EOF
cat > /home/user/npm-lab/widget-kit/src/cli.js <<'EOF'
import { renderWidget } from './index.js';

console.log(renderWidget(process.argv[2] || 'default'));
EOF
cat > /home/user/npm-lab/widget-kit/scripts/build.mjs <<'EOF'
import fs from 'node:fs';

fs.rmSync('dist', { recursive: true, force: true });
fs.mkdirSync('dist', { recursive: true });

fs.writeFileSync(
  'dist/index.mjs',
  "export function renderWidget(name) { return `widget:${name.trim().toLowerCase()}`; }\n",
);
fs.writeFileSync(
  'dist/index.cjs',
  "function renderWidget(name) { return `widget:${name.trim().toLowerCase()}`; }\nmodule.exports = { renderWidget };\n",
);
fs.writeFileSync(
  'dist/index.d.ts',
  "export declare function renderWidget(name: string): string;\n",
);
fs.writeFileSync(
  'dist/cli.cjs',
  "#!/usr/bin/env node\nconst { renderWidget } = require('./index.cjs');\nconsole.log(renderWidget(process.argv[2] || 'default'));\n",
);
fs.chmodSync('dist/cli.cjs', 0o755);
EOF
cat > /home/user/npm-lab/widget-kit/.npmignore <<'EOF'
src/
scripts/
*.log
EOF
cat > /home/user/npm-lab/handoff/acme-widget-kit-1.6.4.tgz <<'EOF'
stale tarball placeholder
EOF
cat > /home/user/npm-lab/handoff/package-manifest.json <<'EOF'
{"stale":true}
EOF
cat > /home/user/npm-lab/handoff/SHA256SUMS <<'EOF'
0000000000000000000000000000000000000000000000000000000000000000  acme-widget-kit-1.6.4.tgz
EOF
chown -R user:user /home/user/npm-lab
SETUP

USER user
WORKDIR /home/user/npm-lab/widget-kit
