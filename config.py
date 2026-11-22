from pathlib import Path
from models import NamingMode

BOOK_ROOT = Path(r"C:\OPDSclient\Books")
PROJECT_ROOT = Path(r"C:\OPDSclient\fb2-renamer")
TEMP_DIR = PROJECT_ROOT / "temp"
NO_SERIES_NAME = "Без серии"
NAMING_MODE = NamingMode.REGULAR_ZIP
SKIP_DUPLICATES = True
