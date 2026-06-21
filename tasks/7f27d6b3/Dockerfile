FROM ubuntu:22.04

LABEL Author="artifact-manager-task"
LABEL Version="1.0"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/data

RUN cat > /home/user/data/artifactory_ops.log <<'EOF'
2023-11-15T10:01:12Z repo-alpha /libs/commons-lang3-3.12.0.jar UPLOAD OK
2023-11-15T10:02:48Z repo-beta /apps/myapp-1.3.1.war DOWNLOAD OK
2023-11-15T10:03:10Z repo-alpha /libs/commons-io-2.11.0.jar UPLOAD FAIL
2023-11-15T10:04:47Z repo-gamma /docker/core-image.tar DELETE OK
2023-11-15T10:05:19Z repo-beta /apps/oldapp-0.9.8.war DELETE FAIL
2023-11-15T10:06:03Z repo-alpha /libs/guava-31.1-jre.jar UPLOAD OK
2023-11-15T10:07:55Z repo-beta /apps/newapp-1.4.0.war DOWNLOAD FAIL
2023-11-15T10:09:12Z repo-gamma /docker/legacy-image.tar UPLOAD OK
2023-11-15T10:10:27Z repo-alpha /libs/log4j-2.17.2.jar DELETE FAIL
2023-11-15T10:11:41Z repo-delta /nuget/packageX.1.0.0.nupkg UPLOAD OK
2023-11-15T10:13:03Z repo-beta /apps/myapp-1.3.2.war DOWNLOAD OK
EOF

RUN chmod 0644 /home/user/data/artifactory_ops.log && \
    chmod 0755 /home/user /home/user/data || true

CMD ["sh", "-c", "chmod 755 /home/user && exec \"$@\"", "--"]