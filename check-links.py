#!/usr/bin/env python3
"""Check for broken internal links and unused images in the docs."""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict

DOCS_DIR = Path(__file__).parent / "Docs"

# Image extensions to track
IMG_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico"}

def find_all_images(root: Path) -> set[Path]:
    """Return all image files under root."""
    images = set()
    for ext in IMG_EXTS:
        for f in root.rglob(f"*{ext}"):
            images.add(f.resolve())
    return images

def find_all_yml_files(root: Path) -> list[Path]:
    """Return all .yml/.yaml files under root."""
    return list(root.rglob("*.yml")) + list(root.rglob("*.yaml"))

def extract_yml_image_refs(yml_path: Path, base: Path = None) -> set[str]:
    """Extract image paths referenced in yml config files (e.g. logo, favicon)."""
    if base is None:
        base = yml_path.parent
    text = yml_path.read_text(encoding="utf-8")
    images = set()
    for m in re.finditer(r'(?:logo|favicon|icon|image|src)\s*:\s*(.+)', text):
        val = m.group(1).strip().strip('"').strip("'")
        if val and not val.startswith(("http://", "https://")):
            # MkDocs Material uses icon: material/something, which isn't a file
            if not any(val.lower().endswith(ext) for ext in IMG_EXTS):
                continue
            target = (base / val).resolve()
            images.add(str(target))
    return images

def find_all_md_files(root: Path) -> list[Path]:
    """Return all .md files under root."""
    return list(root.rglob("*.md"))

def extract_references(md_path: Path) -> tuple[set[str], set[str], set[str]]:
    """
    Parse a markdown file and return:
      - local_links: set of local paths referenced in []() or []() links
      - local_images: set of local image paths referenced in ![]() or <img src="">
      - images_missing_alt: set of image paths (local or remote) missing alt text
    Excludes external URLs (http/https) from local sets, but checks alt text for them.
    """
    text = md_path.read_text(encoding="utf-8")
    # Fenced code is an example, not rendered document links or images.
    text = re.sub(
        r"(?ms)^[ \t]*(?P<fence>`{3,}|~{3,})[^\n]*\n.*?^[ \t]*(?P=fence)[ \t]*(?:\n|$)",
        "",
        text,
    )
    base = md_path.parent

    local_links = set()
    local_images = set()
    images_missing_alt = set()

    # Pattern 1: [text](url)  and  ![alt](url)
    for m in re.finditer(r'(!?)\[(.*?)\]\(([^\)]+)\)', text):
        is_image = m.group(1) == "!"
        alt_text = m.group(2).strip()
        url = m.group(3).strip()

        # Skip external URLs
        if url.startswith(("http://", "https://", "mailto:", "#")):
            if is_image and not alt_text:
                images_missing_alt.add(url)
            continue

        # Strip anchor and query
        clean_url = url.split("#")[0].split("?")[0]
        if not clean_url:
            continue
        target = (base / clean_url).resolve()

        if is_image:
            local_images.add(str(target))
            if not alt_text:
                images_missing_alt.add(str(target))
        else:
            local_links.add(str(target))

    # Pattern 2: <img ...>
    for m in re.finditer(r'<img\s+([^>]+)>', text, re.IGNORECASE):
        attrs = m.group(1)
        src_match = re.search(r'src=["\']([^"\']+)["\']', attrs, re.IGNORECASE)
        alt_match = re.search(r'alt=["\']([^"\']*)["\']', attrs, re.IGNORECASE)

        if src_match:
            url = src_match.group(1).strip()
            has_alt = alt_match is not None and bool(alt_match.group(1).strip())

            if url.startswith(("http://", "https://")):
                if not has_alt:
                    images_missing_alt.add(url)
                continue

            clean_url = url.split("?")[0]
            if not clean_url:
                continue

            target = (base / clean_url).resolve()
            local_images.add(str(target))
            if not has_alt:
                images_missing_alt.add(str(target))

    return local_links, local_images, images_missing_alt

def main():
    md_files = find_all_md_files(DOCS_DIR)
    all_images_on_disk = find_all_images(DOCS_DIR)

    all_refd_links: dict[str, list[str]] = defaultdict(list)   # target → [source files]
    all_refd_images: dict[str, list[str]] = defaultdict(list)
    all_missing_alt: dict[str, list[str]] = defaultdict(list)

    print(f"Scanning {len(md_files)} .md files and {len(all_images_on_disk)} images...\n")

    # Scan .md files
    for md in md_files:
        local_links, local_images, images_missing_alt = extract_references(md)
        rel_md = str(md.relative_to(DOCS_DIR))
        for link in local_links:
            all_refd_links[link].append(rel_md)
        for img in local_images:
            all_refd_images[img].append(rel_md)
        for img in images_missing_alt:
            all_missing_alt[img].append(rel_md)

    # Scan .yml config files (for logo, favicon, etc.)
    # Include both Docs/ subdir and repo root (properdocs.yml lives there)
    yml_files = find_all_yml_files(DOCS_DIR) + find_all_yml_files(DOCS_DIR.parent)
    for yml in yml_files:
        # For yml at repo root, paths are relative to DOCS_DIR (mkdocs docs_dir)
        base = DOCS_DIR if yml.parent == DOCS_DIR.parent else yml.parent
        imgs = extract_yml_image_refs(yml, base)
        rel = str(yml.relative_to(DOCS_DIR.parent)) if DOCS_DIR.parent in yml.parents else str(yml.relative_to(DOCS_DIR))
        for img in imgs:
            all_refd_images[img].append(rel)

    # --- Broken internal links ---
    broken = 0
    print("=" * 60)
    print("BROKEN INTERNAL LINKS")
    print("=" * 60)
    for target, sources in sorted(all_refd_links.items()):
        tpath = Path(target)
        # Check if the target file exists
        if not tpath.exists():
            # Could be a .md file missing the extension — try appending .md
            if not Path(target + ".md").exists():
                print(f"\n  ✗ {Path(target).name}")
                print(f"    Referenced by:")
                for s in sources:
                    print(f"      - {s}")
                broken += 1

    # Check broken images
    for target, sources in sorted(all_refd_images.items()):
        if not Path(target).exists():
            print(f"\n  ✗ (Image) {Path(target).name}")
            print(f"    Referenced by:")
            for s in sources:
                print(f"      - {s}")
            broken += 1

    if broken == 0:
        print("  ✓ No broken internal links or images found.")
    else:
        print(f"\n  Total: {broken} broken link(s)/image(s)")

    # --- Unused images ---
    unused = 0
    print("\n" + "=" * 60)
    print("UNUSED IMAGES")
    print("=" * 60)
    all_refd_image_paths = {Path(p) for p in all_refd_images}
    for img in sorted(all_images_on_disk):
        if img not in all_refd_image_paths:
            rel = img.relative_to(DOCS_DIR)
            print(f"  ✗ {rel} ({img.stat().st_size / 1024:.1f} KB)")
            unused += 1
    if unused == 0:
        print("  ✓ No unused images found.")
    else:
        print(f"\n  Total: {unused} unused image(s)")

    # --- Orphaned Markdown Files ---
    orphans = 0
    print("\n" + "=" * 60)
    print("ORPHANED MARKDOWN FILES (Not in properdocs.yml)")
    print("=" * 60)

    # Parse properdocs.yml for linked md files
    yml_text = ""
    for yml in yml_files:
        yml_text += yml.read_text(encoding="utf-8")

    # Also include files linked from other md files
    all_refd_md_paths = {Path(p) for p in all_refd_links}

    for md in sorted(md_files):
        rel_md = str(md.relative_to(DOCS_DIR))
        # Skip README.md and index.md
        if md.name.lower() in ["readme.md", "index.md"]:
            continue

        # Check if mentioned in properdocs.yml or linked directly
        if rel_md not in yml_text and md not in all_refd_md_paths:
            print(f"  ✗ {rel_md}")
            orphans += 1

    if orphans == 0:
        print("  ✓ No orphaned markdown files found.")
    else:
        print(f"\n  Total: {orphans} orphaned markdown file(s)")

    # --- Empty or Meaningless Documents ---
    empty_docs = 0
    print("\n" + "=" * 60)
    print("EMPTY OR STUB DOCUMENTS")
    print("=" * 60)

    for md in sorted(md_files):
        text = md.read_text(encoding="utf-8").strip()
        # Strip out headers and empty lines
        lines = [line.strip() for line in text.splitlines() if line.strip() and not line.startswith("#")]

        # If file is too small or has less than 2 actual lines of content
        if len(text) < 30 or len(lines) < 2:
            rel_md = str(md.relative_to(DOCS_DIR))
            print(f"  ✗ {rel_md} (Too short/stub: {len(text)} bytes)")
            empty_docs += 1

    if empty_docs == 0:
        print("  ✓ No empty documents found.")
    else:
        print(f"\n  Total: {empty_docs} empty document(s)")

    # --- Missing Alt Text ---
    missing_alt_count = 0
    print("\n" + "=" * 60)
    print("IMAGES MISSING ALT TEXT (Accessibility)")
    print("=" * 60)
    for img, sources in sorted(all_missing_alt.items()):
        img_name = Path(img).name if not img.startswith("http") else img
        print(f"\n  ✗ {img_name}")
        print(f"    Referenced by:")
        for s in sources:
            print(f"      - {s}")
        missing_alt_count += 1

    if missing_alt_count == 0:
        print("  ✓ All images have alt text.")
    else:
        print(f"\n  Total: {missing_alt_count} image(s) missing alt text")

    # --- Corrupted Images (0 Bytes) ---
    corrupted_images = 0
    print("\n" + "=" * 60)
    print("CORRUPTED IMAGES (0 Bytes)")
    print("=" * 60)
    for img in sorted(all_images_on_disk):
        if img.stat().st_size == 0:
            rel = img.relative_to(DOCS_DIR)
            print(f"  ✗ {rel}")
            corrupted_images += 1

    if corrupted_images == 0:
        print("  ✓ No corrupted (0 byte) images found.")
    else:
        print(f"\n  Total: {corrupted_images} corrupted image(s)")

    print()
    return 0 if (broken + unused + orphans + empty_docs + missing_alt_count + corrupted_images) == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
