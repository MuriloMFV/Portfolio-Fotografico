#!/usr/bin/env python3
"""Generate responsive WebP copies without modifying the original photographs.

Requires cwebp (brew install webp) and macOS sips for source dimensions.
Run from any directory: python3 scripts/optimize-images.py
"""

import concurrent.futures
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "fotos" / "optimized"
WIDTHS = (480, 960, 1600, 2400)


def optimize(relative):
    source = ROOT / relative
    metadata = subprocess.check_output(
        ["sips", "-g", "pixelWidth", "-g", "pixelHeight", "-g", "orientation", str(source)],
        text=True,
    )
    width = int(re.search(r"pixelWidth: (\d+)", metadata)[1])
    height = int(re.search(r"pixelHeight: (\d+)", metadata)[1])
    orientation = re.search(r"orientation: (.*)", metadata)[1].strip()
    if orientation not in ("<nil>", "1"):
        raise RuntimeError(f"Normalize EXIF orientation before converting {relative}: {orientation}")
    stem = hashlib.sha256(relative.encode()).hexdigest()[:16]
    variants = []
    for target in sorted({min(width, size) for size in WIDTHS}):
        destination = OUTPUT / f"{stem}-{target}.webp"
        if not destination.exists() or destination.stat().st_mtime < source.stat().st_mtime:
            subprocess.run(
                ["cwebp", "-quiet", "-q", "84", "-m", "6", "-resize", str(target), "0",
                 str(source), "-o", str(destination)],
                check=True,
            )
        variants.append({"width": target, "src": destination.relative_to(ROOT).as_posix()})
    return relative, {"width": width, "height": height, "variants": variants}


def main():
    if not shutil.which("cwebp") or not shutil.which("sips"):
        raise SystemExit("Install cwebp (brew install webp); this script also requires macOS sips.")
    # Keep the source list in the manifest after HTML switches to optimized paths.
    manifest_path = OUTPUT / "manifest.json"
    sources = set(json.loads(manifest_path.read_text()) if manifest_path.exists() else [])
    for page in ROOT.glob("*.html"):
        for raw in re.findall(r'(?:src="|url\([\'\"])(fotos/[^\'\"\n]+)', page.read_text()):
            relative = re.sub(r"\\(.)", r"\1", raw)
            if not relative.startswith("fotos/optimized/"):
                sources.add(relative)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        manifest = dict(pool.map(optimize, sorted(sources)))
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    original = sum((ROOT / name).stat().st_size for name in sources)
    optimized = sum((ROOT / item["src"]).stat().st_size
                    for entry in manifest.values() for item in entry["variants"])
    print(f"{len(sources)} photos: originals {original / 1e6:.1f} MB; all WebP variants {optimized / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
