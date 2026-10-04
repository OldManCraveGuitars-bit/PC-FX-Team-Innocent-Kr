#!/usr/bin/env python3
"""Package the v1.2 stable patch without any copyrighted disc tracks."""
from __future__ import annotations
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT=Path(__file__).resolve().parent
VERSION="v1.2"
FILES=[
    "README.md","CHANGELOG.md","SCREENSHOTS.md",
    *[str(p.relative_to(ROOT)) for p in sorted(ROOT.glob("RELEASE_NOTES_*.md")) if p.name != "RELEASE_NOTES_v0.735-fix1.md"],
    "apply_patch.py","apply_patch.cmd","patch_gui.py",
    f"patches/Team-Innocent-KR-{VERSION}.tipatch",
    f"patches/Team-Innocent-KR-{VERSION}.xdelta",
    *[str(p.relative_to(ROOT)).replace("\\","/") for p in sorted((ROOT/"images").glob("*.png"))],
    *[str(p.relative_to(ROOT)).replace("\\","/") for p in sorted((ROOT/"licenses").glob("*")) if p.is_file()],
]
OUTPUT=ROOT/"dist"/f"Team-Innocent-KR-{VERSION}.zip"
OUTPUT.parent.mkdir(exist_ok=True)
with ZipFile(OUTPUT,"w",ZIP_DEFLATED,compresslevel=9) as archive:
    for name in FILES:
        archive.write(ROOT/name,arcname=name)
    archive.write(ROOT/"dist/gui/Team-Innocent-KR-Patcher.exe",arcname="Team-Innocent-KR-Patcher.exe")
with ZipFile(OUTPUT) as archive:
    bad=archive.testzip()
    if bad:raise ValueError(f"Damaged archive member: {bad}")
    assert len(archive.namelist())==len(FILES)+1
print(OUTPUT,OUTPUT.stat().st_size,len(FILES)+1)
