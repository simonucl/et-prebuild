FROM ubuntu:22.04

# Author="Apptainer Task Prep"
# Description="Environment with initial repository state for Markdown linter task."

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/project/scripts

RUN cat <<'EOF' >/home/user/project/scripts/md_lint
#!/usr/bin/env bash
echo "README.md:1 MD001/heading-increment Header levels should only increment by one level at a time"
echo "CHANGELOG.md:5 MD012/no-multiple-blanks Multiple consecutive blank lines"
EOF

RUN chmod 755 /home/user/project/scripts/md_lint

RUN touch /home/user/project/README.md && \
    touch /home/user/project/CHANGELOG.md

RUN chmod -R a+rwX /home/user/project && \
    chmod 755 /home/user/project/scripts/md_lint