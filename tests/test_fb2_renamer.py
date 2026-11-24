"""
Title:        FB2 Renamer tests
Script Name:  test_fb2_renamer.py
Description:  Unit tests for metadata parsing, naming, and ZIP safety.
Project:      fb2-renamer
Author:       mp
Date:         2026-11-23
Version:      0.2.1
"""

import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from fb2_parser import parse_fb2
from models import BookInfo, NamingMode
from rename_engine import build_target_path, sanitize, store_book
from zip_processor import find_fb2_files, unpack_archive

FB2_XML = '''<?xml version="1.0" encoding="utf-8"?>
<FictionBook xmlns="http://www.gribuser.ru/xml/fictionbook/2.0">
  <description><title-info>
    <author><first-name>Василий</first-name><last-name>Каталкин</last-name></author>
    <book-title>Рерайтер</book-title>
    <sequence name="Рерайтер" number="1" />
  </title-info></description>
</FictionBook>'''


class FB2RenamerTests(unittest.TestCase):
    def test_parse_cyrillic_metadata(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "book.fb2"
            source.write_text(FB2_XML, encoding="utf-8")
            book = parse_fb2(source)
        self.assertEqual(book.title, "Рерайтер")
        self.assertEqual(book.author, "Каталкин Василий")
        self.assertEqual(book.series, "Рерайтер")
        self.assertEqual(book.series_number, 1)

    def test_four_naming_modes(self):
        book = BookInfo("Рерайтер", "Каталкин Василий", "Рерайтер", 1)
        root = Path("/library")
        self.assertEqual(build_target_path(book, root, NamingMode.REGULAR_ZIP), root / "Каталкин Василий" / "Рерайтер" / "01 - Рерайтер.fb2.zip")
        self.assertEqual(build_target_path(book, root, NamingMode.REGULAR_FB2), root / "Каталкин Василий" / "Рерайтер" / "01 - Рерайтер.fb2")
        self.assertEqual(build_target_path(book, root, NamingMode.SERIES_ZIP), root / "Рерайтер" / "01 - Рерайтер.fb2.zip")
        self.assertEqual(build_target_path(book, root, NamingMode.SERIES_FB2), root / "Рерайтер" / "01 - Рерайтер.fb2")

    def test_missing_metadata_fallbacks(self):
        target = build_target_path(BookInfo("", ""), Path("/library"), NamingMode.REGULAR_FB2)
        self.assertIn("Неизвестный автор", str(target))
        self.assertEqual(target, Path("/library") / "Неизвестный автор" / "Без названия.fb2")
        self.assertIn("Без названия", str(target))

    def test_missing_series_omits_series_directory(self):
        book = BookInfo("Книга", "Автор", "", None)
        root = Path("/library")
        self.assertEqual(
            build_target_path(book, root, NamingMode.REGULAR_ZIP),
            root / "Автор" / "Книга.fb2.zip",
        )
        self.assertEqual(
            build_target_path(book, root, NamingMode.SERIES_FB2),
            root / "Книга.fb2",
        )

    def test_windows_invalid_characters_are_replaced(self):
        self.assertEqual(sanitize('a:b?c', 'fallback'), 'a_b_c')

    def test_archive_extract_and_find(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            archive_path = root / "input.zip"
            with ZipFile(archive_path, "w") as archive:
                archive.writestr("nested/Книга.FB2", FB2_XML)
            output = root / "out"
            self.assertEqual(unpack_archive(archive_path, output), 1)
            found = list(find_fb2_files(output))
            self.assertEqual(len(found), 1)
            self.assertEqual(found[0].name, "Книга.FB2")

    def test_zip_path_traversal_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            archive_path = root / "unsafe.zip"
            with ZipFile(archive_path, "w") as archive:
                archive.writestr("../escape.txt", "no")
            with self.assertRaises(ValueError):
                unpack_archive(archive_path, root / "out")
            self.assertFalse((root / "escape.txt").exists())

    def test_store_creates_zipped_output(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source.fb2"
            source.write_text(FB2_XML, encoding="utf-8")
            book = BookInfo("Рерайтер", "Каталкин Василий", "Рерайтер", 1)
            result = store_book(source, book, book_root=root / "library", mode=NamingMode.REGULAR_ZIP)
            self.assertEqual(result, "written")
            target = root / "library" / "Каталкин Василий" / "Рерайтер" / "01 - Рерайтер.fb2.zip"
            self.assertTrue(target.is_file())
            with ZipFile(target) as archive:
                self.assertEqual(archive.namelist(), ["source.fb2"])


if __name__ == "__main__":
    unittest.main()
