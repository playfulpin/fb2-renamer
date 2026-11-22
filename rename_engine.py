import re
import shutil
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from config import BOOK_ROOT, NAMING_MODE, NO_SERIES_NAME, SKIP_DUPLICATES
from models import NamingMode, BookInfo

INVALID_CHARS = r'[<>:"/\\|?*]'

def sanitize(value:str)->str:
    return re.sub(INVALID_CHARS,'_',value).strip()

def build_filename(book:BookInfo)->str:
    title=sanitize(book.title)
    if book.series_number:
        return f'{book.series_number:02d} - {title}'
    return title

def build_target_path(book:BookInfo)->Path:
    filename=build_filename(book)
    series=sanitize(book.series or NO_SERIES_NAME)
    author=sanitize(book.author)
    if NAMING_MODE==NamingMode.REGULAR_ZIP:
        return BOOK_ROOT/author/series/f'{filename}.fb2.zip'
    if NAMING_MODE==NamingMode.REGULAR_FB2:
        return BOOK_ROOT/author/series/f'{filename}.fb2'
    if NAMING_MODE==NamingMode.SERIES_ZIP:
        return BOOK_ROOT/series/f'{filename}.fb2.zip'
    return BOOK_ROOT/series/f'{filename}.fb2'

def store_book(source_fb2:Path, book:BookInfo):
    target=build_target_path(book)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and SKIP_DUPLICATES:
        print(f'SKIP: {target}')
        return
    if target.suffix=='.fb2':
        shutil.move(str(source_fb2), str(target))
        return
    with ZipFile(target,'w',compression=ZIP_DEFLATED) as zf:
        zf.write(source_fb2, arcname=source_fb2.name)
