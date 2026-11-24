"""
Title:        FB2 naming and storage engine
Script Name:  rename_engine.py
Description:  Build destination names and store FB2 books safely.
Project:      fb2-renamer
Author:       mp
Date:         2026-11-23
Version:      0.2.2
"""

import re
import shutil
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from config import NO_AUTHOR_NAME, SERIES_NUMBER_WIDTH, SKIP_DUPLICATES
from models import BookInfo, NamingMode

INVALID_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
RESERVED_NAMES = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}


def sanitize(value: str, fallback: str) -> str:
    """Make a metadata value safe for common Windows filesystems."""
    cleaned = INVALID_CHARS.sub("_", value).strip().rstrip(".")
    cleaned = re.sub(r"\s+", " ", cleaned)
    if not cleaned:
        cleaned = fallback
    if cleaned.upper() in RESERVED_NAMES:
        cleaned = f"_{cleaned}"
    return cleaned


def build_filename(book: BookInfo) -> str:
    """Build the book basename, adding a series number when available."""
    title = sanitize(book.title, "Без названия")
    if book.series_number is not None and book.series_number >= 0:
        return f"{book.series_number:0{SERIES_NUMBER_WIDTH}d} - {title}"
    return title


def build_target_path(
    book: BookInfo, book_root: Path, mode: NamingMode
) -> Path:
    """Build the final path for one book according to the selected mode."""
    filename = build_filename(book)
    series = sanitize(book.series, "") if book.series and book.series.strip() else ""
    author = sanitize(book.author, NO_AUTHOR_NAME)
    zipped = mode in (NamingMode.REGULAR_ZIP, NamingMode.SERIES_ZIP)
    extension = ".fb2.zip" if zipped else ".fb2"

    if series:
        # Series mode groups all books by series; regular mode keeps authors first.
        if mode in (NamingMode.REGULAR_ZIP, NamingMode.REGULAR_FB2):
            target_dir = book_root / author / series
        else:
            target_dir = book_root / series
    else:
        # Standalone books always belong inside their author's directory.
        target_dir = book_root / author

    return target_dir / f"{filename}{extension}"


def store_book(
    source_fb2: Path,
    book: BookInfo,
    *,
    book_root: Path,
    mode: NamingMode,
    dry_run: bool = False,
) -> str:
    """Store one book; return 'written', 'planned', or 'skipped'."""
    target = build_target_path(book, book_root, mode)
    if target.exists() and SKIP_DUPLICATES:
        print(f"SKIP: {target}")
        return "skipped"
    if target.exists():
        raise FileExistsError(f"Destination already exists: {target}")
    if dry_run:
        print(f"DRY RUN: {source_fb2} -> {target}")
        return "planned"

    target.parent.mkdir(parents=True, exist_ok=True)
    if mode in (NamingMode.REGULAR_FB2, NamingMode.SERIES_FB2):
        shutil.copy2(source_fb2, target)
    else:
        with ZipFile(target, "x", compression=ZIP_DEFLATED) as archive:
            archive.write(source_fb2, arcname=source_fb2.name)
    print(f"OK: {target}")
    return "written"
