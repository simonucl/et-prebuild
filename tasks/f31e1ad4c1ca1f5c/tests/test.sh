#!/bin/bash
set -euo pipefail
export LC_ALL=C

mkdir -p /logs/verifier
reward=/logs/verifier/reward.txt

fail() {
  echo 0 > "$reward"
  exit 1
}
trap fail ERR

contrib=/app/repo/src/contrib

test -d "$contrib"

actual_files=$(cd "$contrib" && find . -maxdepth 1 -type f -printf '%P\n' | sort)
expected_files=$'PACKAGES\nPACKAGES.gz\nPACKAGES.rds\nacmeR_0.2.1.tar.gz'
test "$actual_files" = "$expected_files"

tmp_manifest=$(mktemp)
(cd /app/pkg-src && find acmeR -type f -print0 | sort -z | xargs -0 sha256sum) > "$tmp_manifest"
diff -u /app/pkg-src.sha256 "$tmp_manifest"

Rscript --vanilla - <<'RS'
contrib <- "/app/repo/src/contrib"
pkg <- file.path(contrib, "acmeR_0.2.1.tar.gz")

members <- utils::untar(pkg, list = TRUE)
required <- c("acmeR/DESCRIPTION", "acmeR/NAMESPACE",
              "acmeR/R/normalize.R", "acmeR/R/summary.R")
stopifnot(all(required %in% members))
stopifnot(!any(grepl("^/", members)))
stopifnot(!any(strsplit(members, "/", fixed = TRUE) |>
                 vapply(function(parts) any(parts == ".."), logical(1))))

extract_dir <- tempfile("extract-")
dir.create(extract_dir)
utils::untar(pkg, exdir = extract_dir)
desc <- as.data.frame(read.dcf(file.path(extract_dir, "acmeR", "DESCRIPTION")),
                      stringsAsFactors = FALSE)
stopifnot(identical(desc$Package, "acmeR"))
stopifnot(identical(desc$Version, "0.2.1"))
stopifnot(identical(desc$Title, "Acme Edge Sample Normalization Helpers"))
stopifnot(identical(desc$NeedsCompilation, "no"))
for (rel in c("NAMESPACE", "R/normalize.R", "R/summary.R")) {
  stopifnot(identical(readLines(file.path(extract_dir, "acmeR", rel), warn = FALSE),
                      readLines(file.path("/app/pkg-src/acmeR", rel), warn = FALSE)))
}

tmp <- tempfile("repo-")
dir.create(tmp)
file.copy(pkg, tmp, overwrite = TRUE)
tools::write_PACKAGES(tmp, type = "source",
                      fields = c("Package", "Version", "Depends", "Imports",
                                 "License", "Title", "Description",
                                 "NeedsCompilation"),
                      addFiles = TRUE)

expected_packages <- readLines(file.path(tmp, "PACKAGES"), warn = FALSE)
actual_packages <- readLines(file.path(contrib, "PACKAGES"), warn = FALSE)
stopifnot(identical(actual_packages, expected_packages))

actual_gz <- readLines(gzfile(file.path(contrib, "PACKAGES.gz")), warn = FALSE)
stopifnot(identical(actual_gz, actual_packages))

stopifnot(identical(readRDS(file.path(contrib, "PACKAGES.rds")),
                    readRDS(file.path(tmp, "PACKAGES.rds"))))

dcf <- as.data.frame(read.dcf(file.path(contrib, "PACKAGES")), stringsAsFactors = FALSE)
stopifnot(nrow(dcf) == 1)
stopifnot(identical(dcf$Package, "acmeR"))
stopifnot(identical(dcf$Version, "0.2.1"))
stopifnot(identical(dcf$File, "acmeR_0.2.1.tar.gz"))
stopifnot(identical(dcf$NeedsCompilation, "no"))
stopifnot(identical(dcf$MD5sum, tools::md5sum(pkg)[[1]]))

lib <- tempfile("rlib-")
dir.create(lib)
install.packages("acmeR", lib = lib, repos = "file:///app/repo",
                 type = "source", quiet = TRUE)
library(acmeR, lib.loc = lib)
stopifnot(identical(normalize_sample_name(c(" Edge  API ", "Zone/7")), c("edge-api", "zone-7")))
s <- sample_summary(c(2, 4, 8))
stopifnot(identical(s$count, 3L))
stopifnot(identical(s$min, 2))
stopifnot(identical(s$max, 8))
stopifnot(abs(s$mean - 14/3) < 1e-12)
RS

echo 1 > "$reward"
