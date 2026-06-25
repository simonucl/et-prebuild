#!/bin/bash
set -euo pipefail

python3 - <<'PY'
import hashlib
import json
import zipfile
from pathlib import Path

src = Path("/home/user/book_src")
out = Path("/home/user/handoff")
out.mkdir(parents=True, exist_ok=True)
for child in out.iterdir():
    if child.is_file() or child.is_symlink():
        child.unlink()

meta = json.loads((src / "book.json").read_text())

container_xml = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
"""

content_opf = f"""<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="pub-id">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="pub-id">{meta["identifier"]}</dc:identifier>
    <dc:title>{meta["title"]}</dc:title>
    <dc:language>{meta["language"]}</dc:language>
    <dc:creator>{meta["creator"]}</dc:creator>
    <meta property="dcterms:modified">2024-01-01T00:00:00Z</meta>
  </metadata>
  <manifest>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="intro" href="chapters/intro.xhtml" media-type="application/xhtml+xml"/>
    <item id="ops" href="chapters/ops.xhtml" media-type="application/xhtml+xml"/>
    <item id="css" href="styles/book.css" media-type="text/css"/>
    <item id="logo" href="images/logo.svg" media-type="image/svg+xml"/>
  </manifest>
  <spine>
    <itemref idref="intro"/>
    <itemref idref="ops"/>
  </spine>
</package>
"""

nav_xhtml = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en">
<head><title>Field Runbook Navigation</title><link rel="stylesheet" type="text/css" href="styles/book.css"/></head>
<body>
<nav epub:type="toc" id="toc">
<h1>Field Runbook</h1>
<ol>
<li><a href="chapters/intro.xhtml">Introduction</a></li>
<li><a href="chapters/ops.xhtml">Operating Checklist</a></li>
</ol>
</nav>
</body>
</html>
"""

intro_xhtml = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<head><title>Introduction</title><link rel="stylesheet" type="text/css" href="../styles/book.css"/></head>
<body>
<h1>Introduction</h1>
<p>This runbook is used by the Acme field team before a maintenance window.</p>
<ul>
<li>Verify the relay is reachable.</li>
<li>Record the ticket number.</li>
</ul>
</body>
</html>
"""

ops_xhtml = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<head><title>Operating Checklist</title><link rel="stylesheet" type="text/css" href="../styles/book.css"/></head>
<body>
<h1>Operating Checklist</h1>
<p>Follow this checklist in order.</p>
<ol>
<li>Put the relay into drain mode.</li>
<li>Confirm the queue depth is zero.</li>
<li>Resume traffic and capture the health probe.</li>
</ol>
</body>
</html>
"""

entries = [
    ("mimetype", b"application/epub+zip", zipfile.ZIP_STORED),
    ("META-INF/container.xml", container_xml.encode(), zipfile.ZIP_DEFLATED),
    ("OEBPS/content.opf", content_opf.encode(), zipfile.ZIP_DEFLATED),
    ("OEBPS/nav.xhtml", nav_xhtml.encode(), zipfile.ZIP_DEFLATED),
    ("OEBPS/chapters/intro.xhtml", intro_xhtml.encode(), zipfile.ZIP_DEFLATED),
    ("OEBPS/chapters/ops.xhtml", ops_xhtml.encode(), zipfile.ZIP_DEFLATED),
    ("OEBPS/styles/book.css", (src / "assets/book.css").read_bytes(), zipfile.ZIP_DEFLATED),
    ("OEBPS/images/logo.svg", (src / "assets/logo.svg").read_bytes(), zipfile.ZIP_DEFLATED),
]

epub = out / "field-runbook-2.0.0.epub"
with zipfile.ZipFile(epub, "w") as zf:
    for name, data, method in entries:
        info = zipfile.ZipInfo(name, date_time=(2024, 1, 1, 0, 0, 0))
        info.compress_type = method
        info.create_system = 3
        info.external_attr = (0o100644 << 16)
        zf.writestr(info, data)

digest = hashlib.sha256(epub.read_bytes()).hexdigest()
manifest = {
    "name": meta["name"],
    "version": meta["version"],
    "epub": epub.name,
    "sha256": digest,
    "entries": [name for name, _, _ in entries],
}
(out / "manifest.json").write_text(json.dumps(manifest, separators=(",", ":")) + "\n")
PY
