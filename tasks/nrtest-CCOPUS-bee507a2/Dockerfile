FROM ubuntu:24.04

# trsi: pre-create harbor mount points world-writable so non-root-USER envs can be staged
USER root
RUN mkdir -p /solution /tests /logs && chmod 1777 /solution /tests /logs
WORKDIR /app

# Tools the agent may use. dpkg ships in the base image and is the reference
# implementation of Debian version ordering; nothing here solves the task.
RUN apt-get update && apt-get install -y --no-install-recommends \
        coreutils python3 dpkg jq ca-certificates bash \
    && rm -rf /var/lib/apt/lists/*

# Unprivileged working user expected by the scenario.
RUN id user >/dev/null 2>&1 || useradd -m -s /bin/bash user

# ---------------------------------------------------------------------------
# Stage the STARTING state: a read-only build index. Each row is one build
# artifact: <package> <arch> <version> <size_bytes>, tab-separated, with a
# header line. The version strings are full **Debian** version strings and are
# deliberately NOT in sorted order, embedding the classic Debian-ordering traps:
#   * tilde sorts BEFORE everything (1.0~rc1 < 1.0)
#   * an epoch dominates the upstream version (1:1.0 > 2.0)
#   * numeric revision compare (1.0-2 < 1.0-10, not lexical)
#   * build suffixes (1.2.11+deb12u1 > 1.2.11 ; 1.2.13~exp < 1.2.13)
#   * a non-numeric upstream segment (1.0 < 1.0a)
# A naive lexical / SemVer sort gets these wrong.
# ---------------------------------------------------------------------------
RUN set -eu; \
    pool=/home/user/pool; \
    mkdir -p "$pool"; \
    { \
      printf 'package\tarch\tversion\tsize_bytes\n'; \
      printf 'zlibng\tall\t1.2.13\t2200\n'; \
      printf 'libwidget\tamd64\t1.0-2\t1300\n'; \
      printf 'dataproc\tamd64\t1:1.0\t5100\n'; \
      printf 'acme\tamd64\t1.0a\t750\n'; \
      printf 'libwidget\tarm64\t1.0\t1150\n'; \
      printf 'zlibng\tall\t1.2.11+deb12u1\t2100\n'; \
      printf 'libwidget\tamd64\t1.0~rc1\t1100\n'; \
      printf 'dataproc\tamd64\t2.0\t5000\n'; \
      printf 'acme\tamd64\t0.9.8\t650\n'; \
      printf 'libwidget\tamd64\t1.0-10\t1400\n'; \
      printf 'zlibng\tall\t1.2.13~exp\t2150\n'; \
      printf 'libwidget\tarm64\t0.9\t900\n'; \
      printf 'dataproc\tamd64\t1:1.5\t5300\n'; \
      printf 'libwidget\tamd64\t1.0~beta1\t1000\n'; \
      printf 'acme\tamd64\t1.0+deb1\t800\n'; \
      printf 'libwidget\tarm64\t1.0~rc1\t1050\n'; \
      printf 'zlibng\tall\t1.2.11\t2000\n'; \
      printf 'dataproc\tamd64\t1:1.5~rc1\t5200\n'; \
      printf 'libwidget\tamd64\t1.0\t1200\n'; \
      printf 'acme\tamd64\t1.0\t700\n'; \
    } > "$pool/builds.tsv"; \
    chmod 0444 "$pool/builds.tsv"; \
    chmod 0555 "$pool"; \
    chown -R root:root "$pool"

USER user
WORKDIR /home/user
