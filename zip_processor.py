"""
Title:        FB2 ZIP processor
Script Name:  zip_processor.py
Description:  Safely extract archives and locate FB2 documents.
Project:      fb2-renamer
Author:       mp
Date:         2026-11-23
Version:      0.2.0
"""

from pathlib import Path
from zipfile import BadZipFile, ZipFile


def unpack_archive(zip_path: Path, destination: Path) -> int:
    """Extract regular archive members without allowing path traversal."""
    destination = destination.resolve()
    extracted = 0
    try:
        with ZipFile(zip_path, "r") as archive:
            for member in archive.infolist():
                if member.is_dir():
                    continue
                target = (destination / member.filename).resolve()
                if target != destination and destination not in target.parents:
                    raise ValueError(f"Unsafe path in ZIP archive: {member.filename}")
                target.parent.mkdir(parents=True, exist_ok=True)
                with archive.open(member, "r") as source, target.open("wb") as output:
                    while chunk := source.read(1024 * 1024):
                        output.write(chunk)
                extracted += 1
    except BadZipFile as exc:
        raise ValueError(f"Invalid ZIP archive: {zip_path}") from exc
    return extracted


def find_fb2_files(folder: Path):
    """Yield FB2 files recursively, case-insensitively, in stable order."""
    yield from sorted(
        (path for path in folder.rglob("*") if path.is_file() and path.suffix.lower() == ".fb2"),
        key=lambda path: str(path).casefold(),
    )
