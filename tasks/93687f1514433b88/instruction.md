# Deterministic EPUB Handoff

You are preparing an offline EPUB handoff for the Acme field operations runbook. The source material is already staged under:

`/home/user/book_src`

Create the final handoff directory:

`/home/user/handoff`

It must contain exactly these two files:

- `field-runbook-2.0.0.epub`
- `manifest.json`

Build a valid OCF/EPUB ZIP container with no directory entries and this member order:

1. `mimetype`
2. `META-INF/container.xml`
3. `OEBPS/content.opf`
4. `OEBPS/nav.xhtml`
5. `OEBPS/chapters/intro.xhtml`
6. `OEBPS/chapters/ops.xhtml`
7. `OEBPS/styles/book.css`
8. `OEBPS/images/logo.svg`

Packaging requirements:

- `mimetype` must be the first ZIP entry, stored without compression, and contain exactly `application/epub+zip` with no trailing newline.
- Every other ZIP entry must use deflate compression.
- All ZIP member timestamps must be `2024-01-01 00:00:00`.
- All ZIP members must have regular-file permissions `0644`.
- Do not include the draft notes directory or any temporary files.

EPUB content requirements:

- Use `META-INF/container.xml` to point at `OEBPS/content.opf`.
- Use the metadata in `/home/user/book_src/book.json`.
- Convert the two Markdown chapters into XHTML files named `intro.xhtml` and `ops.xhtml`.
- Include a navigation document at `OEBPS/nav.xhtml`.
- Include the CSS and SVG from `/home/user/book_src/assets/` at the paths listed above.

Write `manifest.json` as minified JSON with keys in this order:

`name`, `version`, `epub`, `sha256`, `entries`

The `sha256` value must be the lowercase SHA-256 digest of `field-runbook-2.0.0.epub`. The `entries` array must list the EPUB member names in ZIP order.
