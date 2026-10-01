#!/usr/bin/env python3
"""Apply the Team Innocent KR v0.7 patch to a verified Japanese PC-FX dump.

Only the 14-track original disc files supplied by the user are read. The
included .tipatch holds replacement bytes for changed Track 02 sectors.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import struct
import tempfile
import zlib
from pathlib import Path

BASE = "Team Innocent - The Point of No Return - G.C.P.O.SS (Japan)"
TRACK = f"{BASE} (Track 02).bin"
CUE = f"{BASE}.cue"
PATCH = Path(__file__).resolve().parent / "patches" / "Team-Innocent-KR-v0.7.tipatch"
MAGIC = b"TIKRP07\0"
EXPECTED_SOURCE = "56931167724db296481606b6ba4d873097754faf4a59bd352a030dd8301028aa"
EXPECTED_TARGET = "bdf9335663e7ca405255e9c2eaae7d16556302332a40baebd7af0cfc2427a5f9"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_patch() -> tuple[dict, bytes]:
    with PATCH.open("rb") as stream:
        if stream.read(8) != MAGIC:
            raise ValueError("Invalid .tipatch signature")
        header_size = struct.unpack("<I", stream.read(4))[0]
        if not 0 < header_size < 8192:
            raise ValueError("Invalid patch header length")
        header = json.loads(stream.read(header_size).decode("utf-8"))
        compressed = stream.read()
    if header.get("schema") != "team-innocent-kr-sparse-patch/v1":
        raise ValueError("Unsupported patch format")
    if header.get("source_sha256") != EXPECTED_SOURCE or header.get("target_sha256") != EXPECTED_TARGET:
        raise ValueError("Patch hashes do not match this release")
    if hashlib.sha256(compressed).hexdigest() != header.get("compressed_sha256"):
        raise ValueError("Patch payload checksum mismatch")
    if len(compressed) > 64 * 1024 * 1024:
        raise ValueError("Patch payload is unexpectedly large")
    data = zlib.decompress(compressed)
    if len(data) != header["record_bytes"] or len(data) > 64 * 1024 * 1024:
        raise ValueError("Patch record data size mismatch")
    return header, data


def apply_records(target: Path, header: dict, data: bytes) -> None:
    cursor = 0
    previous_end = 0
    with target.open("r+b") as output:
        for _ in range(header["record_count"]):
            if cursor + 12 > len(data):
                raise ValueError("Truncated patch record")
            offset, size = struct.unpack_from("<QI", data, cursor)
            cursor += 12
            if size == 0 or offset < previous_end or offset + size > header["source_size"]:
                raise ValueError("Invalid patch record range")
            if cursor + size > len(data):
                raise ValueError("Truncated patch data")
            output.seek(offset)
            output.write(data[cursor:cursor + size])
            cursor += size
            previous_end = offset + size
    if cursor != len(data):
        raise ValueError("Unexpected bytes after patch records")


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply Team Innocent KR v0.7 to the original Japanese PC-FX disc.")
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parent / "original_disc",
                        help="Folder containing the original Japanese CUE and all 14 BIN tracks")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "patched_disc",
                        help="New folder for the patched 14-track disc")
    args = parser.parse_args()
    source = args.source.resolve(strict=True)
    output = args.output.resolve(strict=False)
    if not source.is_dir():
        raise ValueError("Source must be a folder")
    if output.exists():
        raise FileExistsError(f"Output already exists: {output}")
    if source == output or source in output.parents:
        raise ValueError("Output must not be inside the source folder")

    filenames = [f"{BASE} (Track {number:02d}).bin" for number in range(1, 15)]
    filenames.append(CUE)
    for name in filenames:
        if not (source / name).is_file():
            raise FileNotFoundError(f"Original disc file missing: {name}")

    header, data = read_patch()
    if header["track_name"] != TRACK or (source / TRACK).stat().st_size != header["source_size"]:
        raise ValueError("This patch expects the original Japanese Track 02")
    print("Checking original Japanese Track 02...")
    if sha256_file(source / TRACK) != EXPECTED_SOURCE:
        raise ValueError("Original Track 02 SHA-256 does not match the supported dump")

    output.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix="team-innocent-kr-v0.7-", dir=output.parent))
    try:
        for name in filenames:
            shutil.copy2(source / name, stage / name)
        apply_records(stage / TRACK, header, data)
        print("Checking patched Track 02...")
        if sha256_file(stage / TRACK) != EXPECTED_TARGET:
            raise ValueError("Patched Track 02 SHA-256 mismatch")
        stage.rename(output)
    except Exception:
        shutil.rmtree(stage, ignore_errors=True)
        raise
    print(f"Done: {output / CUE}")
    print("This is an unverified test release. Keep your original disc files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
