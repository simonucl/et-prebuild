FROM rocker/r-ver:4.4.2

WORKDIR /app

RUN mkdir -p /app/pkg-src/acmeR/R /app/repo/src/contrib && \
    printf '%s\n' \
      'Package: acmeR' \
      'Version: 0.2.1' \
      'Title: Acme Edge Sample Normalization Helpers' \
      'Description: Small helpers for normalizing edge telemetry sample names and producing compact sample summaries for offline handoffs.' \
      'Author: Acme Operations' \
      'Maintainer: Acme Operations <ops@acme.invalid>' \
      'License: MIT' \
      'Encoding: UTF-8' \
      'Depends: R (>= 4.0)' \
      'NeedsCompilation: no' \
      > /app/pkg-src/acmeR/DESCRIPTION && \
    printf '%s\n' \
      'export(normalize_sample_name)' \
      'export(sample_summary)' \
      > /app/pkg-src/acmeR/NAMESPACE && \
    printf '%s\n' \
      'normalize_sample_name <- function(x) {' \
      '  x <- trimws(tolower(as.character(x)))' \
      '  gsub("[^a-z0-9]+", "-", x)' \
      '}' \
      > /app/pkg-src/acmeR/R/normalize.R && \
    printf '%s\n' \
      'sample_summary <- function(values) {' \
      '  values <- as.numeric(values)' \
      '  list(count = length(values), min = min(values), max = max(values), mean = mean(values))' \
      '}' \
      > /app/pkg-src/acmeR/R/summary.R && \
    printf '%s\n' \
      'Package: acmeR' \
      'Version: 0.1.0' \
      'File: acmeR_0.1.0.tar.gz' \
      'MD5sum: stale' \
      > /app/repo/src/contrib/PACKAGES && \
    printf 'not a real package\n' > /app/repo/src/contrib/acmeR_0.1.0.tar.gz && \
    printf 'stale metadata\n' > /app/repo/src/contrib/PACKAGES.gz && \
    printf 'stale rds\n' > /app/repo/src/contrib/PACKAGES.rds && \
    (cd /app/pkg-src && find acmeR -type f -print0 | sort -z | xargs -0 sha256sum) > /app/pkg-src.sha256
