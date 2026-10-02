#!/usr/bin/env python3
"""Package the v0.76 test patch without any copyrighted disc tracks."""
from __future__ import annotations
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT=Path(__file__).resolve().parent
VERSION="v0.76"
FILES=[
    "README.md",f"RELEASE_NOTES_{VERSION}.md",
    "apply_patch.py","apply_patch.cmd","patch_gui.py",
    f"patches/Team-Innocent-KR-{VERSION}.tipatch",
    f"patches/Team-Innocent-KR-{VERSION}.xdelta",
    *[str(p.relative_to(ROOT)).replace("\\","/") for p in sorted((ROOT/"images").glob("*.png"))],
    *[str(p.relative_to(ROOT)).replace("\\","/") for p in sorted((ROOT/"licenses").glob("*")) if p.is_file()],
]
OUTPUT=ROOT/"dist"/f"Team-Innocent-KR-{VERSION}-test.zip"
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
