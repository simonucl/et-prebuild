# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Create home directory
# ------------------------------------------------------------------
RUN mkdir -p /home/user

# ------------------------------------------------------------------
# 1. Create the working directory structure and populate artifacts.tsv
# ------------------------------------------------------------------
RUN mkdir -p /home/user/repos-inventory

RUN cat > /home/user/repos-inventory/artifacts.tsv <<'ARTIFACTS'
repo_id	artifact_name	version	size_kb	sha256
core	com.acme:libcrypto	1.2.0	8640	7b5f96b26d9f5a37c1e420a63daa45f64f1ac2f9d8bded0372cd5152c3d9d7c1
core	com.acme:libhttp	2.5.1	12800	3cfc7dbeab9e4d0482a6f8f2dfe6d1b62a6e2ce4b3c0e5e4b21dd9c649c34337
utils	org.tools:zipper	0.9.8	5120	d7a4b5a8934dd94dcd4b4a6e4b3e2c8fd2e9adf3edd5c6b1b3a9e5d8f6a7b2d3
utils	org.tools:packer	1.0.0	20480	e6f2d3b4a5c6979876543210abcdefabcdef01234567890fedcba9876543210
ml	ai.deep:torch	1.9.0	73400	c1d2e3f40506070809101112131415161718191a1b1c1d1e1f20212223242526
ml	ai.deep:onnx	1.8.1	9200	aabbccddeeff00112233445566778899aabbccddeeff00112233445566778899
java	org.apache:log4j	2.14.1	800	99887766554433221100ffeeddccbbaa99887766554433221100ffeeddccbbaa
java	com.google:guava	30.1.1	2650	11223344556677889900aabbccddeeff00112233445566778899aabbccddeeff
db	com.mysql:mysql-connector	8.0.25	9800	2233445566778899aabbccddeeff00112233445566778899aabbccddeeff
db	org.postgres:pgjdbc	42.2.20	5020	33445566778899aabbccddeeff00112233445566778899aabbccddeeff00
ARTIFACTS

RUN chmod 0777 /home/user/repos-inventory && \
    chmod 0644 /home/user/repos-inventory/artifacts.tsv

# ------------------------------------------------------------------
# 2. Install Python and pytest
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Permissions and metadata
# ------------------------------------------------------------------
RUN chmod 755 /home/user

LABEL Author="repos-inventory-setup"