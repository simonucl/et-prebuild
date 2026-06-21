FROM ubuntu:22.04

# %post
RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/user-accounts

RUN cat > /home/user/user-accounts/VERSION <<'EOF'
1.5.2
EOF

RUN cat > /home/user/user-accounts/CHANGELOG.md <<'EOF'
## [1.5.2] - 2023-09-28
- Improve password hashing

## [1.5.1] - 2023-09-20
- Add MFA enrolment command

## [1.5.0] - 2023-09-15
- Initial public release
EOF

RUN chmod -R 777 /home/user/user-accounts

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# %environment
RUN chmod 755 /home/user
ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=UTF-8