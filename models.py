"""
Title:        FB2 Renamer data models
Script Name:  models.py
Description:  Shared data structures and naming modes.
Project:      fb2-renamer
Author:       mp
Date:         2026-11-23
Version:      0.2.0
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class NamingMode(str, Enum):
    """Supported destination layouts and output formats."""

    REGULAR_ZIP = "regular_zip"
    REGULAR_FB2 = "regular_fb2"
    SERIES_ZIP = "series_zip"
    SERIES_FB2 = "series_fb2"


@dataclass(frozen=True)
class BookInfo:
    """Metadata extracted from an FB2 document."""

    title: str
    author: str
    series: Optional[str] = None
    series_number: Optional[int] = None
