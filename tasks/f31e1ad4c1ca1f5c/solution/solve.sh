#!/bin/bash
set -euo pipefail

repo=/app/repo/src/contrib
src=/app/pkg-src/acmeR

rm -rf "$repo"
mkdir -p "$repo"

build_dir=$(mktemp -d)
trap 'rm -rf "$build_dir"' EXIT

(
  cd "$build_dir"
  R CMD build --no-manual --no-resave-data --no-build-vignettes "$src"
)
cp "$build_dir"/acmeR_0.2.1.tar.gz "$repo"/

Rscript -e 'tools::write_PACKAGES("/app/repo/src/contrib", type = "source", fields = c("Package", "Version", "Depends", "Imports", "License", "Title", "Description", "NeedsCompilation"), addFiles = TRUE)'
