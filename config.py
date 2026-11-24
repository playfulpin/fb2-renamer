"""
Title:        FB2 Renamer configuration
Script Name:  config.py
Description:  Default paths and processing settings.
Project:      fb2-renamer
Author:       mp
Date:         2026-11-23
Version:      0.2.0
"""

from pathlib import Path

from models import NamingMode

PROJECT_ROOT = Path(__file__).resolve().parent
BOOK_ROOT = Path(r"C:\OPDSclient\Books")
TEMP_DIR = PROJECT_ROOT / "temp"
NO_SERIES_NAME = "Без серии"
NO_AUTHOR_NAME = "Неизвестный автор"
NAMING_MODE = NamingMode.REGULAR_ZIP
SKIP_DUPLICATES = True
LOG_LEVEL = "WARNING"
SERIES_NUMBER_WIDTH = 2
