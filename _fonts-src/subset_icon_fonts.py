#!/usr/bin/env python3
"""Subset the Font Awesome and Academicons web fonts to the icons the site uses.

The full fonts (~700 icons) are kept here in _fonts-src/ (Jekyll does not
publish underscore directories). This script scans the templates and content
for `fa-*` / `ai-*` class names, keeps only those glyphs, and writes the
.woff2/.woff/.ttf files that browsers download into assets/fonts/.

Run it again after adding a new icon anywhere on the site:

    pip install fonttools brotli
    python3 _fonts-src/subset_icon_fonts.py
"""
import re
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_fonts-src"
OUT = ROOT / "assets" / "fonts"
SCAN_DIRS = ["_includes", "_layouts", "_pages", "_posts", "_portfolio",
             "_publications", "_talks", "_teaching", "_drafts", "assets/js"]
SCAN_FILES = ["_config.yml", "index.html"]


def used_classes(prefix):
    # Literal classes (`fa-github`) plus names that templates build at render
    # time, e.g. `fa-{{ include.icon | default: 'file-text' }}` in _includes/toc
    # and `{% include toc icon="gears" %}` in content.
    pattern = re.compile(r"\b" + prefix + r"-([a-z0-9-]+)"
                         r"|" + prefix + r"-\{\{[^}]*default:\s*['\"]([a-z0-9-]+)['\"]"
                         r"|\bicon=['\"]([a-z0-9-]+)['\"]")
    names = set()
    paths = [ROOT / f for f in SCAN_FILES]
    for d in SCAN_DIRS:
        paths += [p for p in (ROOT / d).rglob("*") if p.is_file()]
    for p in paths:
        # Some Jekyll includes have no extension (_includes/toc, _includes/base_path).
        if p.exists() and p.suffix in {"", ".html", ".md", ".yml", ".js", ".markdown"}:
            for groups in pattern.findall(p.read_text(errors="ignore")):
                names.update(g for g in groups if g)
    return names


def codepoints(names, mapping):
    return sorted({mapping[n] for n in names if n in mapping})


def fa_mapping():
    text = (ROOT / "_sass/vendor/font-awesome/_variables.scss").read_text()
    return {m[0]: int(m[1], 16) for m in re.findall(r'\$fa-var-([a-z0-9-]+):\s*"\\([0-9a-f]+)"', text)}


def ai_mapping():
    text = (ROOT / "assets/css/academicons.css").read_text()
    return {m[0]: int(m[1], 16) for m in re.findall(r'\.ai-([a-z0-9-]+):before\s*\{\s*content:\s*"\\([0-9a-f]+)"', text)}


def write_subsets(src_name, out_stem, unicodes, flavors):
    options = subset.Options()
    options.layout_features = ["*"]
    options.name_IDs = ["*"]
    options.notdef_outline = True
    for flavor, ext in flavors:
        font = TTFont(SRC / src_name)
        sub = subset.Subsetter(options)
        sub.populate(unicodes=unicodes)
        sub.subset(font)
        font.flavor = flavor
        out = OUT / f"{out_stem}.{ext}"
        font.save(out)
        print(f"{out.relative_to(ROOT)}: {len(unicodes)} icons, {out.stat().st_size} bytes")


FLAVORS = [("woff2", "woff2"), ("woff", "woff"), (None, "ttf")]
write_subsets("fontawesome-webfont.ttf", "fontawesome-webfont",
              codepoints(used_classes("fa"), fa_mapping()), FLAVORS)
write_subsets("academicons.ttf", "academicons",
              codepoints(used_classes("ai"), ai_mapping()), FLAVORS)
