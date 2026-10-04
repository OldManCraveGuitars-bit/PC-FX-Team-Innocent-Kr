#!/usr/bin/env python3
"""Build a deterministic sparse Track 02 patch from the verified Japanese disc."""
from __future__ import annotations
import argparse, hashlib, json, struct, zlib
from pathlib import Path

MAGIC = b"TIKR1200"
SECTOR = 2352
TRACK = "Team Innocent - The Point of No Return - G.C.P.O.SS (Japan) (Track 02).bin"


def build(source: Path, target: Path, output: Path) -> dict:
    if source.stat().st_size != target.stat().st_size:
        raise ValueError("Source and target must have equal length")
    source_hash = hashlib.sha256()
    target_hash = hashlib.sha256()
    records = []
    start = None
    changed = bytearray()
    with source.open("rb") as old, target.open("rb") as new:
        offset = 0
        while before := old.read(SECTOR):
            after = new.read(len(before))
            if len(after) != len(before):
                raise ValueError("Target ends early")
            source_hash.update(before)
            target_hash.update(after)
            if before != after:
                if start is None:
                    start = offset
                changed.extend(after)
            elif start is not None:
                records.append((start, bytes(changed)))
                start = None
                changed.clear()
            offset += len(before)
        if new.read(1):
            raise ValueError("Target has trailing bytes")
    if start is not None:
        records.append((start, bytes(changed)))
    data = b"".join(struct.pack("<QI", offset, len(value)) + value for offset, value in records)
    compressed = zlib.compress(data, level=9)
    header = {
        "schema": "team-innocent-kr-sparse-patch/v1",
        "version": "v1.2",
        "track_name": TRACK,
        "source_size": source.stat().st_size,
        "source_sha256": source_hash.hexdigest(),
        "target_sha256": target_hash.hexdigest(),
        "record_count": len(records),
        "record_bytes": len(data),
        "compressed_sha256": hashlib.sha256(compressed).hexdigest(),
    }
    encoded = json.dumps(header, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(MAGIC + struct.pack("<I", len(encoded)) + encoded + compressed)
    return header


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("target", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    print(json.dumps(build(args.source, args.target, args.output), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
