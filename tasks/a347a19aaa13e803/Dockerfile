FROM ubuntu:24.04

WORKDIR /home/user

RUN apt-get update && apt-get install -y \
    bash \
    ca-certificates \
    coreutils \
    findutils \
    gzip \
    nodejs \
    npm \
    python3 \
    tar \
  && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash user

RUN mkdir -p /home/user/npm-lab/src/acme-logship/bin \
    /home/user/npm-lab/src/acme-logship/lib \
    /home/user/npm-lab/src/acme-logship/notes \
    /home/user/npm-lab/dist

RUN cat > /home/user/npm-lab/src/acme-logship/package.json <<'EOF'
{
  "name": "acme-logship",
  "version": "0.5.9",
  "description": "Offline log shipping CLI",
  "license": "UNLICENSED",
  "bin": {
    "logship": "bin/logship-cli.js"
  },
  "files": [
    "bin/",
    "lib/",
    "README.md",
    "LICENSE",
    "notes/"
  ]
}
EOF

RUN cat > /home/user/npm-lab/src/acme-logship/bin/logship.js <<'EOF'
#!/usr/bin/env node
const { formatLine } = require("../lib/index.js");

const [level = "info", ...rest] = process.argv.slice(2);
process.stdout.write(formatLine(level, rest.join(" ")) + "\n");
EOF

RUN cat > /home/user/npm-lab/src/acme-logship/lib/index.js <<'EOF'
function formatLine(level, message) {
  return `${level}: ${message}`;
}

module.exports = { formatLine };
EOF

RUN cat > /home/user/npm-lab/src/acme-logship/README.md <<'EOF'
# acme-logship

Offline log shipping command-line utility.
EOF

RUN cat > /home/user/npm-lab/src/acme-logship/LICENSE <<'EOF'
MIT
EOF

RUN cat > /home/user/npm-lab/src/acme-logship/notes/private-release-notes.txt <<'EOF'
Do not ship this internal note.
EOF

RUN chmod 0644 /home/user/npm-lab/src/acme-logship/bin/logship.js \
    /home/user/npm-lab/src/acme-logship/lib/index.js \
    /home/user/npm-lab/src/acme-logship/package.json \
    /home/user/npm-lab/src/acme-logship/README.md \
    /home/user/npm-lab/src/acme-logship/LICENSE \
    /home/user/npm-lab/src/acme-logship/notes/private-release-notes.txt \
  && chown -R user:user /home/user/npm-lab

USER user
