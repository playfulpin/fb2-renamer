#!/usr/bin/env python3
"""
Title:        FB2 Renamer
Script Name:  main.py
Description:  Organize FB2 books from an input ZIP archive.
Project:      fb2-renamer
Author:       mp
Date:         2026-11-23
Version:      0.2.0
"""

import argparse
import logging
import sys
import tempfile
from pathlib import Path

from config import BOOK_ROOT, LOG_LEVEL, NAMING_MODE, TEMP_DIR
from fb2_parser import parse_fb2
from models import NamingMode
from rename_engine import store_book
from zip_processor import find_fb2_files, unpack_archive


def parse_arguments() -> argparse.Namespace:
    """Parse command-line options."""
    parser = argparse.ArgumentParser(
        description="Organize FB2 books from a ZIP archive using FB2 metadata."
    )
    parser.add_argument("archive", type=Path, help="Input ZIP archive")
    parser.add_argument(
        "--mode",
        choices=[mode.value for mode in NamingMode],
        default=NAMING_MODE.value,
        help=f"Output naming mode (default: {NAMING_MODE.value})",
    )
    parser.add_argument(
        "--book-root",
        type=Path,
        default=BOOK_ROOT,
        help=f"Output library directory (default: {BOOK_ROOT})",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Report planned operations without writing output"
    )
    parser.add_argument(
        "--keep-temp", action="store_true", help="Keep extracted files in the configured temp directory"
    )
    parser.add_argument("--verbose", action="store_true", help="Enable informational logging")
    return parser.parse_args()


def main() -> int:
    """Run the archive processing workflow."""
    args = parse_arguments()
    logging.basicConfig(
        level=logging.INFO if args.verbose else getattr(logging, LOG_LEVEL.upper(), logging.WARNING),
        format="%(levelname)s: %(message)s",
    )

    archive = args.archive.expanduser().resolve()
    if not archive.is_file():
        logging.error("Input archive does not exist: %s", archive)
        return 2
    if not archive.name.lower().endswith(".zip"):
        logging.error("Input file must be a ZIP archive: %s", archive)
        return 2

    args.book_root = args.book_root.expanduser().resolve()
    args.mode = NamingMode(args.mode)
    args.book_root.mkdir(parents=True, exist_ok=True) if not args.dry_run else None

    if args.keep_temp:
        TEMP_DIR.mkdir(parents=True, exist_ok=True)
        work_dir = TEMP_DIR
        cleanup = False
    else:
        TEMP_DIR.mkdir(parents=True, exist_ok=True)
        temp_context = tempfile.TemporaryDirectory(prefix="fb2-renamer-", dir=TEMP_DIR)
        work_dir = Path(temp_context.name)
        cleanup = True

    processed = skipped = failed = 0
    try:
        extracted = unpack_archive(archive, work_dir)
        fb2_files = list(find_fb2_files(work_dir))
        if not fb2_files:
            logging.warning("No FB2 files found in %s", archive)
        for fb2_file in fb2_files:
            try:
                book = parse_fb2(fb2_file)
                result = store_book(
                    fb2_file,
                    book,
                    book_root=args.book_root,
                    mode=args.mode,
                    dry_run=args.dry_run,
                )
                if result == "skipped":
                    skipped += 1
                else:
                    processed += 1
            except (OSError, ValueError, UnicodeError) as exc:
                failed += 1
                logging.error("Could not process %s: %s", fb2_file.name, exc)
        logging.info("Extracted %d archive members", extracted)
    except (OSError, ValueError) as exc:
        logging.error("Archive processing failed: %s", exc)
        return 2
    finally:
        if cleanup:
            temp_context.cleanup()

    print(f"Processed: {processed}; skipped: {skipped}; failed: {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
