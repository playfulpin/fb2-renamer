from dataclasses import dataclass
from enum import Enum
from typing import Optional

class NamingMode(Enum):
    REGULAR_ZIP = "regular_zip"
    REGULAR_FB2 = "regular_fb2"
    SERIES_ZIP = "series_zip"
    SERIES_FB2 = "series_fb2"

@dataclass
class BookInfo:
    title: str
    author: str
    series: Optional[str] = None
    series_number: Optional[int] = None
