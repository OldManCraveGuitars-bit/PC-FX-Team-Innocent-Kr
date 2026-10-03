#!/usr/bin/env python3
"""Apply the Team Innocent KR v0.85 patch to a verified Japanese PC-FX dump.

The original disc is only read. A temporary copy is validated before it
becomes the output folder, so failed or cancelled runs leave no partial disc.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import struct
import sys
import tempfile
import zlib
from pathlib import Path
from typing import Callable

BASE = "Team Innocent - The Point of No Return - G.C.P.O.SS (Japan)"
TRACK = f"{BASE} (Track 02).bin"
CUE = f"{BASE}.cue"
PATCH = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent)) / "patches" / "Team-Innocent-KR-v0.85.tipatch"
MAGIC = b"TIKR0850"
EXPECTED_SOURCE = "56931167724db296481606b6ba4d873097754faf4a59bd352a030dd8301028aa"
EXPECTED_TARGET = "d581f895f41f857eb76d2a7fec96dacb405222febcc091587769036dec3a67ec"
Progress = Callable[[int, str, float], None]
Cancellation = Callable[[], bool]


class PatchCancelled(Exception):
    """The user stopped the patch before the output folder was published."""


def check_cancelled(cancelled: Cancellation | None) -> None:
    if cancelled and cancelled():
        raise PatchCancelled()


def sha256_file(path: Path, tick: Callable[[int], None] | None = None,
                cancelled: Cancellation | None = None) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 * 1024 * 1024):
            check_cancelled(cancelled)
            digest.update(block)
            if tick:
                tick(len(block))
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


def apply_records(target: Path, header: dict, data: bytes,
                  tick: Callable[[float], None] | None = None,
                  cancelled: Cancellation | None = None) -> None:
    cursor = 0
    previous_end = 0
    with target.open("r+b") as output:
        for index in range(header["record_count"]):
            check_cancelled(cancelled)
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
            if tick:
                tick((index + 1) / header["record_count"])
    if cursor != len(data):
        raise ValueError("Unexpected bytes after patch records")


def apply_patch(source: Path, output: Path, progress: Progress | None = None,
                cancelled: Cancellation | None = None) -> Path:
    source = source.resolve(strict=True)
    output = output.resolve(strict=False)

    def report(step: int, label: str, fraction: float) -> None:
        if progress:
            progress(step, label, min(1.0, max(0.0, fraction)))

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

    report(0, "원본 디스크 검사", 0)
    source_size = (source / TRACK).stat().st_size
    verified = 0

    def source_tick(size: int) -> None:
        nonlocal verified
        verified += size
        report(0, "원본 디스크 검사", verified / source_size)

    if sha256_file(source / TRACK, source_tick, cancelled) != EXPECTED_SOURCE:
        raise ValueError("Original Track 02 SHA-256 does not match the supported dump")

    check_cancelled(cancelled)
    output.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix="team-innocent-kr-v0.85-", dir=output.parent))
    try:
        total_copy = sum((source / name).stat().st_size for name in filenames)
        copied = 0
        report(1, "디스크 파일 복사", 0)
        for name in filenames:
            check_cancelled(cancelled)
            with (source / name).open("rb") as input_file, (stage / name).open("wb") as output_file:
                while block := input_file.read(4 * 1024 * 1024):
                    check_cancelled(cancelled)
                    output_file.write(block)
                    copied += len(block)
                    report(1, "디스크 파일 복사", copied / total_copy)
            shutil.copystat(source / name, stage / name)

        report(2, "한국어 패치 적용", 0)
        apply_records(stage / TRACK, header, data,
                      lambda fraction: report(2, "한국어 패치 적용", fraction), cancelled)

        report(3, "완성된 디스크 검사", 0)
        verified = 0

        def target_tick(size: int) -> None:
            nonlocal verified
            verified += size
            report(3, "완성된 디스크 검사", verified / source_size)

        if sha256_file(stage / TRACK, target_tick, cancelled) != EXPECTED_TARGET:
            raise ValueError("Patched Track 02 SHA-256 mismatch")
        check_cancelled(cancelled)
        stage.rename(output)
    except Exception:
        shutil.rmtree(stage, ignore_errors=True)
        raise
    return output / CUE


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply Team Innocent KR v0.85 to the original Japanese PC-FX disc.")
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parent / "original_disc",
                        help="Folder containing the original Japanese CUE and all 14 BIN tracks")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "patched_disc",
                        help="New folder for the patched 14-track disc")
    args = parser.parse_args()
    cue = apply_patch(args.source, args.output,
                      lambda step, label, fraction: print(f"{label}: {fraction:.0%}") if fraction == 1 else None)
    print(f"Done: {cue}")
    print("This is an unverified test release. Keep your original disc files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
