# Repair the Offline Go Module Proxy

The source for the internal Go module is staged at:

`/app/module-src`

A broken static Go module proxy is staged at:

`/app/goproxy/example.internal/edge/ratelimit/@v`

Repair the proxy for module `example.internal/edge/ratelimit` version `v0.9.0`. Do not use the network, and do not modify anything under `/app/module-src`.

The final proxy directory must contain exactly these files:

- `list`
- `v0.9.0.info`
- `v0.9.0.mod`
- `v0.9.0.zip`
- `proxy-manifest.json`

Requirements:

1. `list` must advertise only `v0.9.0` with LF line endings and exactly one trailing newline.
2. `v0.9.0.info` must be minified JSON with exactly one trailing newline:
   `{"Version":"v0.9.0","Time":"2026-06-01T10:30:00Z"}`
3. `v0.9.0.mod` must exactly match `/app/module-src/go.mod`.
4. `v0.9.0.zip` must be a deterministic Go module ZIP archive containing the staged source files under the root prefix `example.internal/edge/ratelimit@v0.9.0/`.
   The ZIP member order must be:
   - `example.internal/edge/ratelimit@v0.9.0/go.mod`
   - `example.internal/edge/ratelimit@v0.9.0/limiter.go`
   - `example.internal/edge/ratelimit@v0.9.0/limiter_test.go`
   - `example.internal/edge/ratelimit@v0.9.0/README.md`
   Each member must use timestamp `1980-01-01T00:00:00Z` and Unix mode `0644`.
5. `proxy-manifest.json` must be minified JSON with exactly one trailing newline. Its top-level keys must appear in this order:
   `module`, `version`, `files`, `zip_sha256`, `mod_sha256`, `info_sha256`

The manifest `files` array must list the four source files in the same order as the ZIP, using paths relative to `/app/module-src`, byte sizes, and SHA-256 digests of the source file bytes. The three manifest digest fields must be SHA-256 hex digests of the final `v0.9.0.zip`, `v0.9.0.mod`, and `v0.9.0.info` files.

When finished, an offline Go command using `GOPROXY=file:///app/goproxy` should be able to download `example.internal/edge/ratelimit@v0.9.0`.
